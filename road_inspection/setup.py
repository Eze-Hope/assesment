from setuptools import find_packages, setup

package_name = 'road_inspection'

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
    maintainer='kasm-user',
    maintainer_email='kasm-user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mover = road_inspection.mover:main',
            'opencv_test = road_inspection.opencv_test:main',
            'tf_listener = road_inspection.tf_listener:main',
            'mover_with_pose = road_inspection.mover_with_pose:main',
            'image_projection1 = road_inspection.image_projection1:main',
        ],
    },
)
