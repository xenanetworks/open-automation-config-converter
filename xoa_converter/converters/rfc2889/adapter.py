import hashlib
import types
from decimal import Decimal
from typing import Dict, TYPE_CHECKING
from .model import (
    ValkyrieConfiguration2889 as old_model,
    LegacyFrameSizesOptions,
)
from ..common import (
    TestParameters,
    PortIdentity,
    convert_protocol_segments,
)

if TYPE_CHECKING:
    from .model import (
        LegacyPortEntity,
    )


class Converter2889:
    def __init__(self, source_config: str, target_module: types.ModuleType) -> None:
        self.id_map = {}
        self.module = target_module
        self.data = old_model.parse_raw(source_config)

    def __gen_port_identity(self) -> Dict[str, "PortIdentity"]:
        chassis_id_map = {}
        port_identity = {}

        for chassis_info in self.data.chassis_manager.chassis_list:
            chassis_id = hashlib.md5(
                f"{chassis_info.host_name}:{chassis_info.port_number}".encode("utf-8")
            ).hexdigest()
            chassis_id_map[chassis_info.chassis_id] = chassis_id
        count = 0
        chassis_id_list = list(chassis_id_map.values())
        for p_info in self.data.port_handler.entity_list:
            port = p_info.port_ref
            port.chassis_id = chassis_id_map[port.chassis_id]
            identity = PortIdentity(
                tester_id=port.chassis_id,
                tester_index=chassis_id_list.index(port.chassis_id),
                module_index=port.module_index,
                port_index=port.port_index,
            )

            self.id_map[p_info.item_id] = (f"{identity.name}", f"p{count}")
            port_identity[f"p{count}"] = identity
            count += 1
        return port_identity

    def __gen_ipv4_addr(self, entity: "LegacyPortEntity"):
        return self.module.IPV4AddressProperties.construct(
            address=entity.ip_v4_address,
            routing_prefix=entity.ip_v4_routing_prefix,
            gateway=entity.ip_v4_gateway if entity.ip_v4_gateway else "0.0.0.0",
            public_address=entity.public_ip_address
            if entity.public_ip_address
            else "0.0.0.0",
            public_routing_prefix=entity.public_ip_routing_prefix,
            remote_loop_address=entity.remote_loop_ip_address
            if entity.remote_loop_ip_address
            else "0.0.0.0",
        )

    def __gen_ipv6_addr(self, entity: "LegacyPortEntity"):
        return self.module.IPV6AddressProperties.construct(
            address=entity.ip_v6_address,
            routing_prefix=entity.ip_v6_routing_prefix,
            gateway=entity.ip_v6_gateway if entity.ip_v6_gateway else "::",
            public_address=entity.public_ip_address_v6
            if entity.public_ip_address_v6
            else "::",
            public_routing_prefix=entity.public_ip_routing_prefix_v6,
            remote_loop_address=entity.remote_loop_ip_address_v6
            if entity.remote_loop_ip_address_v6
            else "::",
        )

    def __gen_port_conf(self, entity: "LegacyPortEntity"):
        profile_id = self.data.stream_profile_handler.profile_assignment_map.get(f"guid_{entity.item_id}")
        return self.module.PortConfiguration.construct(
            port_slot=self.id_map[entity.item_id][1],
            peer_config_slot=self.id_map[entity.pair_peer_id][0]
            if entity.pair_peer_id and entity.pair_peer_id in self.id_map
            else "",
            port_group=entity.port_group,
            port_speed_mode=entity.port_speed,
            ipv4_properties=self.__gen_ipv4_addr(entity),
            ipv6_properties=self.__gen_ipv6_addr(entity),
            ip_gateway_mac_address=entity.ip_gateway_mac_address,
            reply_arp_requests=bool(entity.reply_arp_requests),
            reply_ping_requests=bool(entity.reply_ping_requests),
            remote_loop_mac_address=entity.remote_loop_mac_address,
            interframe_gap=entity.inter_frame_gap,
            speed_reduction_ppm=entity.adjust_ppm,
            pause_mode_enabled=entity.pause_mode_on,
            latency_offset_ms=entity.latency_offset,
            fec_mode=self.module.FECModeStr[entity.fec_mode.name.lower()],
            port_rate_cap_enabled=bool(entity.enable_port_rate_cap),
            port_rate_cap_value=entity.port_rate_cap_value,
            port_rate_cap_profile=self.module.PortRateCapProfile[entity.port_rate_cap_profile.name.lower()],
            port_rate_cap_unit=self.module.PortRateCapUnit[entity.port_rate_cap_unit.name.lower()],
            auto_neg_enabled=bool(entity.auto_neg_enabled),
            anlt_enabled=bool(entity.anlt_enabled),
            mdi_mdix_mode=entity.mdi_mdix_mode,
            broadr_reach_mode=entity.brr_mode,
            profile_id=profile_id,
            item_id=entity.item_id,
        )

    def __gen_port_config(self) -> Dict:
        port_conf: Dict = {}
        for entity in self.data.port_handler.entity_list:
            port_conf[self.id_map[entity.item_id][0]] = self.__gen_port_conf(entity)
        return port_conf

    def __gen_frame_size(self):
        packet_size = self.data.test_options.packet_sizes
        packet_size_type = packet_size.packet_size_type
        fz = packet_size.mixed_length_config.frame_sizes
        return self.module.FrameSizeConfiguration.construct(
            packet_size_type=self.module.PacketSizeType[packet_size_type.name.lower()],
            custom_packet_sizes=packet_size.custom_packet_sizes,
            fixed_packet_start_size=packet_size.sw_packet_start_size,
            fixed_packet_end_size=packet_size.sw_packet_end_size,
            fixed_packet_step_size=packet_size.sw_packet_step_size,
            varying_packet_min_size=packet_size.hw_packet_min_size,
            varying_packet_max_size=packet_size.hw_packet_max_size,
            mixed_sizes_weights=packet_size.mixed_sizes_weights,
            mixed_length_config=LegacyFrameSizesOptions(**fz),
        )

    def __gen_rate_definition(self):
        return self.module.RateDefinition.construct(
            rate_type=self.module.StreamRateType[self.data.test_options.rate_definition.rate_type.name.lower()],
            rate_fraction=self.data.test_options.rate_definition.rate_fraction,
            rate_pps=self.data.test_options.rate_definition.rate_pps,
            rate_bps_l1=self.data.test_options.rate_definition.rate_bps_l1,
            rate_bps_l1_unit=self.module.PortRateCapUnit[ self.data.test_options.rate_definition.rate_bps_l1_unit.name.lower() ],
            rate_bps_l2=self.data.test_options.rate_definition.rate_bps_l2,
            rate_bps_l2_unit= self.module.PortRateCapUnit[ self.data.test_options.rate_definition.rate_bps_l2_unit.name.lower() ],
        )

    def __gen_general_test_config(self):
        return self.module.GeneralTestConfiguration.construct(
            frame_sizes=self.__gen_frame_size(),
            rate_definition=self.__gen_rate_definition(),
            latency_mode=self.data.test_options.latency_mode,
            toggle_sync_state=self.data.test_options.toggle_sync_state,
            sync_off_duration=self.data.test_options.sync_off_duration,
            sync_on_duration=self.data.test_options.sync_on_duration,
            should_stop_on_los=self.data.test_options.should_stop_on_los,
            port_reset_delay=self.data.test_options.port_reset_delay,
            use_port_sync_start=self.data.test_options.use_port_sync_start,
            port_stagger_steps=self.data.test_options.port_stagger_steps,
            use_micro_tpld_on_demand=self.data.test_options.flow_creation_options.use_micro_tpld_on_demand,
            tid_allocation_scope=self.module.TidAllocationScope[ self.data.tid_allocation_scope.name.lower() ],
        )

    def __gen_rate_iteration_options(self, rate_iteration_options):
        return self.module.RateIterationOptions.construct(
            initial_value=rate_iteration_options.initial_value,
            minimum_value=rate_iteration_options.minimum_value,
            maximum_value=rate_iteration_options.maximum_value,
            value_resolution=rate_iteration_options.value_resolution,
            use_pass_threshold=rate_iteration_options.use_pass_threshold,
            pass_threshold=rate_iteration_options.pass_threshold,
        )
    def __gen_rate_sweep_option(self, rate_sweep_options):
        return self.module.NewRateSweepOptions.construct(
            start_value=Decimal(rate_sweep_options.start_value),
            end_value=Decimal(rate_sweep_options.end_value),
            step_value=Decimal(rate_sweep_options.step_value),
        )

    def __gather_test_case_common_config(self, test_case_config):
        return dict(
            enabled=test_case_config.enabled,
            duration_type=self.module.DurationType[ test_case_config.duration_type.name.lower() ],
            duration=test_case_config.duration,
            duration_time_unit=test_case_config.duration_time_unit,
            duration_frames=test_case_config.duration_frames,
            duration_frame_unit=self.module.DurationFrameUnit[ test_case_config.duration_frame_unit.name.lower() ],
            iterations=test_case_config.iterations,
            item_id=test_case_config.item_id,
            label=test_case_config.label,
        )

    def __gen_rate_test(self):
        rate_test_config = self.data.test_options.test_type_option_map.rate_test
        all_rate_sub_tests = []

        for sub_test in rate_test_config.rate_sub_test_handler.rate_sub_tests:
            rate_sub_test = self.module.RateSubTestConfiguration.construct(
                topology=sub_test.topology,
                direction=self.module.TrafficDirection[ sub_test.direction.name.lower() ],
                port_role_handler=sub_test.port_role_handler,
                throughput_test_enabled=sub_test.throughput_test_enabled,
                rate_iteration_options=self.__gen_rate_iteration_options(
                    sub_test.rate_iteration_options
                ),
                forwarding_test_enabled=sub_test.forwarding_test_enabled,
                rate_sweep_options=self.__gen_rate_sweep_option(sub_test.rate_sweep_options),
                **self.__gather_test_case_common_config(sub_test),
            )
            all_rate_sub_tests.append(rate_sub_test)

        return self.module.RateTestConfiguration.construct(
            sub_test=all_rate_sub_tests,
            **self.__gather_test_case_common_config(rate_test_config),
        )

    def __gen_congestion_control(self):
        return self.module.CongestionControlConfiguration.construct(
            port_role_handler=self.data.test_options.test_type_option_map.congestion_control.port_role_handler,
            **self.__gather_test_case_common_config(self.data.test_options.test_type_option_map.congestion_control)
        )

    def __gen_forward_pressure(self):
        forward_pressure = self.data.test_options.test_type_option_map.forward_pressure
        return self.module.ForwardPressureConfiguration.construct(
            port_role_handler=forward_pressure.port_role_handler,
            interframe_gap_delta=forward_pressure.interframe_gap_delta,
            acceptable_rx_max_util_delta=forward_pressure.acceptable_rx_max_util_delta,
            **self.__gather_test_case_common_config(forward_pressure)
        )

    def __gen_max_forwarding_rate(self):
        max_forwarding_rate = self.data.test_options.test_type_option_map.max_forwarding_rate
        return self.module.MaxForwardingRateConfiguration.construct(
            port_role_handler=max_forwarding_rate.port_role_handler,
            use_throughput_as_start_value=max_forwarding_rate.use_throughput_as_start_value,
            rate_sweep_options=self.__gen_rate_sweep_option(max_forwarding_rate.rate_sweep_options),
            **self.__gather_test_case_common_config(max_forwarding_rate),
        )

    def __gen_address_caching_capacity(self):
        address_caching_capacity = self.data.test_options.test_type_option_map.address_caching_capacity
        return self.module.AddressCachingCapacityConfiguration.construct(
            port_role_handler=address_caching_capacity.port_role_handler,
            address_iteration_options=self.__gen_rate_iteration_options(address_caching_capacity.address_iteration_options),
            rate_sweep_options=self.__gen_rate_sweep_option(address_caching_capacity.rate_sweep_options),
            learn_mac_base_address=address_caching_capacity.learn_mac_base_address,
            test_port_mac_mode=address_caching_capacity.test_port_mac_mode,
            learning_port_dmac_mode=address_caching_capacity.learning_port_dmac_mode,
            learning_sequence_port_dmac_mode=address_caching_capacity.learning_sequence_port_dmac_mode,
            learning_rate_fps=address_caching_capacity.learning_rate_fps,
            toggle_sync_state=address_caching_capacity.toggle_sync_state,
            sync_off_duration=address_caching_capacity.sync_off_duration,
            sync_on_duration=address_caching_capacity.sync_on_duration,
            switch_test_port_roles=address_caching_capacity.switch_test_port_roles,
            dut_aging_time=address_caching_capacity.dut_aging_time,
            fast_run_resolution_enabled=address_caching_capacity.fast_run_resolution_enabled,
            **self.__gather_test_case_common_config(address_caching_capacity),
        )

    def __gen_address_learning_rate(self):
        address_learning_rate = self.data.test_options.test_type_option_map.address_learning_rate
        return self.module.AddressLearningRateConfiguration.construct(
            port_role_handler=address_learning_rate.port_role_handler,
            rate_iteration_options=self.__gen_rate_iteration_options(address_learning_rate.rate_iteration_options),
            address_sweep_options=self.module.NewRateSweepOptions.parse_obj(address_learning_rate.address_sweep_options.dict()),
            learn_mac_base_address=address_learning_rate.learn_mac_base_address,
            test_port_mac_mode=address_learning_rate.test_port_mac_mode,
            learning_port_dmac_mode=address_learning_rate.learning_port_dmac_mode,
            learning_sequence_port_dmac_mode=address_learning_rate.learning_sequence_port_dmac_mode,
            learning_rate_fps=address_learning_rate.learning_rate_fps,
            toggle_sync_state=address_learning_rate.toggle_sync_state,
            sync_off_duration=address_learning_rate.sync_off_duration,
            sync_on_duration=address_learning_rate.sync_on_duration,
            switch_test_port_roles=address_learning_rate.switch_test_port_roles,
            dut_aging_time=address_learning_rate.dut_aging_time,
            only_use_capacity=address_learning_rate.only_use_capacity,
            set_end_address_to_capacity=address_learning_rate.set_end_address_to_capacity,
            **self.__gather_test_case_common_config(address_learning_rate),
        )

    def __gen_errored_frames_filtering(self):
        errored_frames_filtering = self.data.test_options.test_type_option_map.errored_frames_filtering
        return self.module.ErroredFramesFilteringConfiguration.construct(
            port_role_handler=errored_frames_filtering.port_role_handler,
            rate_sweep_options=self.module.NewRateSweepOptions.parse_obj(errored_frames_filtering.rate_sweep_options.dict()),
            oversize_test_enabled=errored_frames_filtering.oversize_test_enabled,
            max_frame_size=errored_frames_filtering.max_frame_size,
            oversize_span=errored_frames_filtering.oversize_span,
            min_frame_size=errored_frames_filtering.min_frame_size,
            undersize_span=errored_frames_filtering.undersize_span,
            **self.__gather_test_case_common_config(errored_frames_filtering),
        )

    def __gen_broadcast_forwarding(self):
        broadcast_forwarding = self.data.test_options.test_type_option_map.broadcast_forwarding
        return self.module.BroadcastForwardingConfiguration.construct(
            port_role_handler=broadcast_forwarding.port_role_handler,
            rate_iteration_options=self.__gen_rate_iteration_options(broadcast_forwarding.rate_iteration_options),
            **self.__gather_test_case_common_config(broadcast_forwarding),
        )

    def __gen_test_types_config(self):
        return self.module.TestSuitesConfiguration.construct(
            rate_test=self.__gen_rate_test(),
            congestion_control=self.__gen_congestion_control(),
            forward_pressure=self.__gen_forward_pressure(),
            max_forwarding_rate=self.__gen_max_forwarding_rate(),
            address_caching_capacity=self.__gen_address_caching_capacity(),
            address_learning_rate=self.__gen_address_learning_rate(),
            errored_frames_filtering=self.__gen_errored_frames_filtering(),
            broadcast_forwarding=self.__gen_broadcast_forwarding(),
        )

    def gen(self) -> "TestParameters":
        port_identities = self.__gen_port_identity()
        config = self.module.TestSuiteConfiguration2889.construct(
            ports_configuration=self.__gen_port_config(),
            protocol_segments=convert_protocol_segments(self.data.stream_profile_handler, self.module),
            general_test_configuration=self.__gen_general_test_config(),
            test_suites_configuration=self.__gen_test_types_config(),
        )
        return TestParameters(username="RFC-2889", config=config, port_identities=port_identities)

