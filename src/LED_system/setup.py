from setuptools import setup

package_name = 'LED_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ranish',
    maintainer_email='ranish075bei@ioepc.edu.np',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "battery_node = LED_system.battery:main",
            "pannel = LED_system.led_pannel:main"
        ],
    },
)
