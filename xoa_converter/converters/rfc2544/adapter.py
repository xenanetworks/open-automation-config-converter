import hashlib
from typing import List, Dict, Union, TYPE_CHECKING
from .model import LegacyModel2544 as old_model
from ..common import convert_protocol_segments

if TYPE_CHECKING:
    from .model import (
        LegacyBack2Back,
        LegacyLatency,
        LegacyLoss,
        LegacyRateIterationOptions,
        LegacyRateSweepOptions,
        LegacyPortEntity,
        LegacyThroughput,
    )


def convert_base_mac_address(mac_address: str) -> str:
    prefix = [hex(int(i)) for i in mac_address.split(",")]
    return ":".join([p.replace("0x", "").zfill(2).lower() for p in prefix])


class Converter2544:
    def __init__(self, source_config: str) -> None:
        self.id_map = {}
        self.data = old_model.parse_raw(source_config)

    def __gen_frame_size(self) -> Dict:
        packet_size = self.data.test_options.packet_sizes
        packet_size_type = packet_size.packet_size_type
        fz = packet_size.mixed_length_config.frame_sizes
        return dict(
            packet_size_type=packet_size_type.name.lower(),
            custom_packet_sizes=packet_size.custom_packet_sizes,
            fixed_packet_start_size=packet_size.sw_packet_start_size,
            fixed_packet_end_size=packet_size.sw_packet_end_size,
            fixed_packet_step_size=packet_size.sw_packet_step_size,
            varying_packet_min_size=packet_size.hw_packet_min_size,
            varying_packet_max_size=packet_size.hw_packet_max_size,
            mixed_sizes_weights=packet_size.mixed_sizes_weights,
            mixed_length_config=fz,
        )

    def __gen_multi_stream_config(self) -> Dict:
        flow_option = self.data.test_options.flow_creation_options
        return dict(
            enable_multi_stream=flow_option.enable_multi_stream,
            per_port_stream_count=flow_option.per_port_stream_count,
            multi_stream_address_offset=flow_option.multi_stream_address_offset,
            multi_stream_address_increment=flow_option.multi_stream_address_increment,
            multi_stream_mac_base_address=convert_base_mac_address(
                flow_option.multi_stream_mac_base_address
            ),
        )

    def __gen_port_sync_config(self) -> Dict:
        test_options = self.data.test_options

        return dict(
            delay_after_sync_on_second=test_options.sync_on_duration,
            toggle_port_sync=test_options.toggle_sync_state,
            sync_off_duration_second=test_options.sync_off_duration,
        )

    def __gen_test_config(self) -> Dict:
        test_options = self.data.test_options
        flow_option = test_options.flow_creation_options
        payload = test_options.payload_definition
        learning_options = test_options.learning_options
        topology = self.data.test_options.topology_config.topology.lower()
        direction = self.data.test_options.topology_config.direction.name.lower()
        outer_loop_mode = test_options.outer_loop_mode
        tid_allocation_scope = self.data.tid_allocation_scope
        flow_creation_type = flow_option.flow_creation_type
        port_sync_config = self.__gen_port_sync_config()
        frame_size = self.__gen_frame_size()
        return dict(
            flow_creation_type=flow_creation_type.name.lower(),
            tid_allocation_scope=tid_allocation_scope.name.lower(),
            mac_base_address=convert_base_mac_address(flow_option.mac_base_address),
            enable_speed_reduction_sweep=test_options.enable_speed_reduct_sweep,
            use_port_sync_start=test_options.use_port_sync_start,
            port_stagger_steps=test_options.port_stagger_steps,
            outer_loop_mode=outer_loop_mode.name.lower(),
            mac_learning_mode=learning_options.mac_learning_mode.name.lower(),
            mac_learning_frame_count=learning_options.mac_learning_retries,
            toggle_port_sync_config=port_sync_config,
            learning_rate_pct=learning_options.learning_rate_percent,
            learning_duration_second=learning_options.learning_duration,
            use_flow_based_learning_preamble=learning_options.use_flow_based_learning_preamble,
            flow_based_learning_frame_count=learning_options.flow_based_learning_frame_count,
            delay_after_flow_based_learning_ms=learning_options.flow_based_learning_delay,
            arp_refresh_enabled=learning_options.arp_refresh_enabled,
            arp_refresh_period_second=learning_options.arp_refresh_period,
            use_gateway_mac_as_dmac=flow_option.use_gateway_mac_as_dmac,
            should_stop_on_los=test_options.should_stop_on_los,
            delay_after_port_reset_second=test_options.port_reset_delay,
            topology=topology,
            direction=direction,
            frame_sizes=frame_size,
            use_micro_tpld_on_demand=flow_option.use_micro_tpld_on_demand,
            payload_type=payload.payload_type,
            payload_pattern="".join(
                [
                    hex(int(i)).replace("0x", "").zfill(2)
                    for i in payload.payload_pattern.split(",")
                ]
            ),
            multi_stream_config=self.__gen_multi_stream_config(),
        )

    def __gen_rate_sweep_option(
        self,
        rate_sweep_options: "LegacyRateSweepOptions",
        burst_resolution: float = 0.0,
    ) -> Dict:
        return dict(
            start_value_pct=rate_sweep_options.start_value,
            end_value_pct=rate_sweep_options.end_value,
            step_value_pct=rate_sweep_options.step_value,
            burst_resolution=burst_resolution,
        )

    def __gen_common_option(
        self,
        test_type_conf: Union[
            "LegacyThroughput", "LegacyLatency", "LegacyLoss", "LegacyBack2Back"
        ],
    ) -> Dict:
        duration_type = test_type_conf.duration_type.name.lower()

        is_time_duration = test_type_conf.duration_type.is_time_duration
        return dict(
            duration_type=duration_type,
            duration=test_type_conf.duration
            if is_time_duration
            else test_type_conf.duration_frames,
            duration_unit=test_type_conf.duration_time_unit.name.lower()
            if is_time_duration
            else test_type_conf.duration_frame_unit.name.lower(),
            iterations=test_type_conf.iterations,
        )

    def __gen_rate_iteration_options(
        self, rate_iteration_options: "LegacyRateIterationOptions"
    ) -> Dict:
        return dict(
            search_type=rate_iteration_options.search_type.name.lower(),
            result_scope=rate_iteration_options.result_scope.name.lower(),
            initial_value_pct=rate_iteration_options.initial_value,
            minimum_value_pct=rate_iteration_options.minimum_value,
            maximum_value_pct=rate_iteration_options.maximum_value,
            value_resolution_pct=rate_iteration_options.value_resolution,
        )

    def __gen_throughput(self, throughput: "LegacyThroughput") -> Dict:
        rate_iteration_options = throughput.rate_iteration_options
        return dict(
            test_type=throughput.test_type.name.lower(),
            enabled=throughput.enabled,
            common_options=self.__gen_common_option(throughput),
            rate_iteration_options=self.__gen_rate_iteration_options(
                rate_iteration_options
            ),
            use_pass_threshold=rate_iteration_options.use_pass_threshold,
            pass_threshold_pct=rate_iteration_options.pass_threshold,
            acceptable_loss_pct=rate_iteration_options.acceptable_loss,
            collect_latency_jitter="LatencyCounters"
            in throughput.report_property_options,
        )

    def __gen_latency(self, latency: "LegacyLatency") -> Dict:
        return dict(
            test_type=latency.test_type.name.lower(),
            enabled=latency.enabled,
            common_options=self.__gen_common_option(latency),
            rate_sweep_options=self.__gen_rate_sweep_option(latency.rate_sweep_options),
            latency_mode=latency.latency_mode.lower(),
            use_relative_to_throughput=latency.rate_relative_tput_max_rate,
        )

    def __gen_loss(self, loss: "LegacyLoss") -> Dict:
        return dict(
            test_type=loss.test_type.name.lower(),
            enabled=loss.enabled,
            common_options=self.__gen_common_option(loss),
            rate_sweep_options=self.__gen_rate_sweep_option(loss.rate_sweep_options),
            use_pass_fail_criteria=loss.use_pass_fail_criteria,
            acceptable_loss_pct=loss.acceptable_loss,
            acceptable_loss_type=loss.acceptable_loss_type.lower(),
            use_gap_monitor=loss.use_gap_monitor,
            gap_monitor_start_microsec=loss.gap_monitor_start,
            gap_monitor_stop_frames=loss.gap_monitor_stop,
        )

    def __gen_back_to_back(self, back_to_back: "LegacyBack2Back") -> Dict:
        return dict(
            test_type=back_to_back.test_type.name.lower(),
            enabled=back_to_back.enabled,
            common_options=self.__gen_common_option(back_to_back),
            rate_sweep_options=self.__gen_rate_sweep_option(
                back_to_back.rate_sweep_options, (back_to_back.burst_resolution)
            ),
        )

    def __gen_test_type_config(self) -> Dict:
        test_type_option_map = self.data.test_options.test_type_option_map
        return dict(
            throughput_test=self.__gen_throughput(test_type_option_map.throughput),
            latency_test=self.__gen_latency(test_type_option_map.latency),
            frame_loss_rate_test=self.__gen_loss(test_type_option_map.loss),
            back_to_back_test=self.__gen_back_to_back(test_type_option_map.back2_back),
        )

    def __gen_port_identity(self) -> List:
        chassis_id_map = {}
        port_identity = {}

        for chassis_info in self.data.chassis_manager.chassis_list:
            chassis_id = hashlib.md5(
                f"{chassis_info.host_name}:{chassis_info.port_number}".encode("utf-8")
            ).hexdigest()
            chassis_id_map[chassis_info.chassis_id] = chassis_id
        chassis_id_list = list(chassis_id_map.values())
        for count, p_info in enumerate(self.data.port_handler.entity_list):
            port = p_info.port_ref
            port.chassis_id = chassis_id_map[port.chassis_id]
            identity = dict(
                tester_id=port.chassis_id,
                tester_index=chassis_id_list.index(port.chassis_id),
                module_index=port.module_index,
                port_index=port.port_index,
            )

            self.id_map[p_info.item_id] = (
                f"c-P-{identity['tester_index']}-{identity['module_index']}-{identity['port_index']}",
                f"p{count}",
            )
            port_identity[f"p{count}"] = identity
        return port_identity

    def __gen_ipv4_addr(self, entity: "LegacyPortEntity") -> Dict:
        return dict(
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

    def __gen_ipv6_addr(self, entity: "LegacyPortEntity") -> Dict:
        return dict(
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
        profile_id = self.data.stream_profile_handler.profile_assignment_map.get(
            f"guid_{entity.item_id}"
        )
        return dict(
            port_slot=self.id_map[entity.item_id][1],
            peer_config_slot=self.id_map[entity.pair_peer_id][0]
            if entity.pair_peer_id and entity.pair_peer_id in self.id_map
            else "",
            port_group=entity.port_group.lower(),
            port_speed_mode=entity.port_speed.lower(),
            ipv4_properties=self.__gen_ipv4_addr(entity),
            ipv6_properties=self.__gen_ipv6_addr(entity),
            ip_gateway_mac_address=entity.ip_gateway_mac_address,
            reply_arp_requests=bool(entity.reply_arp_requests),
            reply_ping_requests=bool(entity.reply_ping_requests),
            remote_loop_mac_address=entity.remote_loop_mac_address,
            inter_frame_gap=entity.inter_frame_gap,
            speed_reduction_ppm=entity.adjust_ppm,
            pause_mode_enabled=entity.pause_mode_on,
            latency_offset_ms=entity.latency_offset,
            fec_mode=entity.fec_mode.name.lower(),
            port_rate_cap_enabled=bool(entity.enable_port_rate_cap),
            port_rate_cap_value=entity.port_rate_cap_value,
            port_rate_cap_profile=entity.port_rate_cap_profile.name.lower(),
            port_rate_cap_unit=entity.port_rate_cap_unit.name.lower().lstrip("field_"),
            auto_neg_enabled=bool(entity.auto_neg_enabled),
            anlt_enabled=bool(entity.anlt_enabled),
            mdi_mdix_mode=entity.mdi_mdix_mode.lower(),
            broadr_reach_mode=entity.brr_mode.lower(),
            profile_id=profile_id,
        )

    def __generate_port_config(self) -> Dict:
        port_conf: Dict = {}
        for entity in self.data.port_handler.entity_list:
            port_conf[self.id_map[entity.item_id][0]] = self.__gen_port_conf(entity)
        return port_conf

    def gen(self) -> Dict:
        port_identities = self.__gen_port_identity()
        test_conf = self.__gen_test_config()
        config = dict(
            protocol_segments=convert_protocol_segments(
                self.data.stream_profile_handler
            ),
            test_configuration=test_conf,
            test_types_configuration=self.__gen_test_type_config(),
            ports_configuration=self.__generate_port_config(),
        )
        return dict(username="hello", config=config, port_identities=port_identities)
