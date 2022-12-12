import setuptools

def main():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="xoa-converter",
        description="Xena OpenAutomation test configuration converter let you easily migrate your Valkyrie test suites config files (.v2544, .v2889, .v3918, and .v1564) into XOA.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Frank Chen, Maureen Chen, Artem Constantinov",
        author_email="fch@xenanewtorks.com, mch@xenanetworks.com, aco@xenanetworks.com",
        maintainer="Xena Networks",
        maintainer_email="support@xenanetworks.com",
        url="https://github.com/xenanetworks/open-automation-config-converter",
        packages=setuptools.find_packages(),
        license='Apache 2.0',
        install_requires=["pydantic>=1.8.2", "datamodel-code-generator"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
        ],
        python_requires=">=3.8.9",
        include_package_data=True,
    )

if __name__ == '__main__':
    main()

