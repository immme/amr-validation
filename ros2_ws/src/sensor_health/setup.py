from setuptools import find_packages, setup

package_name = 'sensor_health'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Minseok Lee',
    maintainer_email='dev.immme@gmail.com',
    description='Fake sensor and health check nodes for validating ROS 2 topic streams',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            # 실행 이름 = 모듈 경로:호출할 함수
            'fake_sensor = sensor_health.fake_sensor:main',
            'sensor_receiver = sensor_health.sensor_receiver:main',
            'fake_scan = sensor_health.fake_scan:main',
            'scan_receiver = sensor_health.scan_receiver:main',
        ],
    },
)
