# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import pytest

from utils.exceptions import FailedTestError


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary', 'custom-full')], indirect=True)
class TestSampleScriptsLinux:
    def test_benchmark_app_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/samples/scripts/run_sample_benchmark_app.sh -d CPU',
             ], self.test_benchmark_app_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_benchmark_app_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/samples/scripts/run_sample_benchmark_app.sh -d GPU',
             ], self.test_benchmark_app_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_benchmark_app_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/samples/scripts/run_sample_benchmark_app.sh -d MYRIAD',
             ], self.test_benchmark_app_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_benchmark_app_hddl(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('umask 0000 && /opt/intel/openvino/samples/scripts/run_sample_benchmark_app.sh '
                  '-d HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_benchmark_app_hddl.__name__, **kwargs,
        )

    def test_squeezenet_cpu(self, tester, image, install_openvino_dependencies):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/samples/scripts/run_sample_squeezenet.sh -d CPU',
             ], self.test_squeezenet_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_squeezenet_gpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/samples/scripts/run_sample_squeezenet.sh -d GPU',
             ], self.test_squeezenet_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR',
                           reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_squeezenet_vpu(self, tester, image, install_openvino_dependencies):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             '/opt/intel/openvino/samples/scripts/run_sample_squeezenet.sh -d MYRIAD',
             ], self.test_squeezenet_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_squeezenet_hddl(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('umask 0000 && /opt/intel/openvino/samples/scripts/run_sample_squeezenet.sh '
                  '-d HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_squeezenet_hddl.__name__, **kwargs,
        )


@pytest.mark.usefixtures('_is_image_os', '_is_distribution')
@pytest.mark.parametrize('_is_image_os', [('ubuntu18', 'ubuntu20', 'rhel8')], indirect=True)
@pytest.mark.parametrize('_is_distribution', [('dev', 'proprietary', 'custom-full')], indirect=True)
class TestSamplesLinux:
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_hello_classification_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car.png'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/scripts/car.png CPU'),
             ], self.test_hello_classification_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_hello_classification_cpp_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car.png'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/scripts/car.png GPU'),
             ], self.test_hello_classification_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_classification_cpp_vpu(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/scripts/car.png MYRIAD'),
             ], self.test_hello_classification_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_classification_cpp_hddl(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             bash('umask 0000 && /root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '/opt/intel/openvino/samples/scripts/car.png HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_hello_classification_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_min_product_version')
    @pytest.mark.parametrize('_min_product_version', ['2021.2'], indirect=True)
    def test_hello_classification_cpp_fail(self, tester, image, caplog, bash,
                                           install_openvino_dependencies, download_picture):
        with pytest.raises(FailedTestError):
            tester.test_docker_image(
                image,
                [install_openvino_dependencies,
                 bash('python3 -m pip install --no-cache-dir cmake setuptools && '
                      'cd /opt/intel/openvino/samples/cpp && '
                      '/opt/intel/openvino/samples/cpp/build_samples.sh'),
                 bash('python3 -m pip install --no-cache-dir '
                      '-r /opt/intel/openvino/extras/open_model_zoo/tools/model_tools/requirements.in && '
                      'omz_downloader --name vehicle-attributes-recognition-barrier-0039 --precisions FP32 '
                      '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
                 download_picture('car.png'),
                 bash('/root/inference_engine_cpp_samples_build/intel64/Release/hello_classification '
                      '/root/inference_engine_cpp_samples_build/intel64/Release/intel/'
                      'vehicle-attributes-recognition-barrier-0039/FP32/'
                      'vehicle-attributes-recognition-barrier-0039.xml '
                      '/opt/intel/openvino/samples/scripts/car.png CPU'),
                 ], self.test_hello_classification_cpp_fail.__name__,
            )
        if 'Sample supports models with 1 output only' not in caplog.text:
            pytest.fail('Sample supports models with 1 output only')

    def test_hello_reshape_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/scripts/car_1.bmp CPU 1'),
             ], self.test_hello_reshape_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_hello_reshape_cpp_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/scripts/car_1.bmp GPU 1'),
             ], self.test_hello_reshape_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_reshape_cpp_vpu(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/scripts/car_1.bmp MYRIAD 1'),
             ], self.test_hello_reshape_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_hello_reshape_cpp_hddl(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('umask 0000 && /root/inference_engine_cpp_samples_build/intel64/Release/hello_reshape_ssd '
                  '/root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '/opt/intel/openvino/samples/scripts/car_1.bmp HDDL 1 && rm -f /dev/shm/hddl_*'),
             ], self.test_hello_reshape_cpp_hddl.__name__, **kwargs,
        )

    def test_object_detection_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d CPU'),
             ], self.test_object_detection_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    def test_object_detection_cpp_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             download_picture('car_1.bmp'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d GPU'),
             ], self.test_object_detection_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_object_detection_cpp_vpu(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d MYRIAD'),
             ], self.test_object_detection_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_object_detection_cpp_hddl(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name vehicle-detection-adas-0002 --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('umask 0000 && /root/inference_engine_cpp_samples_build/intel64/Release/object_detection_sample_ssd '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/intel/vehicle-detection-adas-0002/FP16/'
                  'vehicle-detection-adas-0002.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_object_detection_cpp_hddl.__name__, **kwargs,
        )

    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_classification_async_cpp_cpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d CPU'),
             ], self.test_classification_async_cpp_cpu.__name__,
        )

    @pytest.mark.gpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    def test_classification_async_cpp_gpu(self, tester, image, install_openvino_dependencies, bash, download_picture):
        kwargs = {'devices': ['/dev/dri:/dev/dri'], 'mem_limit': '3g'}
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             download_picture('car_1.bmp'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d GPU'),
             ], self.test_classification_async_cpp_gpu.__name__, **kwargs,
        )

    @pytest.mark.vpu
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.xfail_log(pattern='Can not init Myriad device: NC_ERROR', reason='Sporadic error on MYRIAD device')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_classification_async_cpp_vpu(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'device_cgroup_rules': ['c 189:* rmw'],
                  'volumes': ['/dev/bus/usb:/dev/bus/usb'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             bash('/root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d MYRIAD'),
             ], self.test_classification_async_cpp_vpu.__name__, **kwargs,
        )

    @pytest.mark.hddl
    @pytest.mark.xfail_log(pattern='Error: Download',
                           reason='Network problems when downloading alexnet files')
    @pytest.mark.usefixtures('_is_not_image_os')
    @pytest.mark.parametrize('_is_not_image_os', [('rhel8')], indirect=True)
    def test_classification_async_cpp_hddl(self, tester, image, install_openvino_dependencies, bash):
        kwargs = {'devices': ['/dev/ion:/dev/ion'],
                  'volumes': ['/var/tmp:/var/tmp', '/dev/shm:/dev/shm'], 'mem_limit': '3g'}  # nosec # noqa: S108
        tester.test_docker_image(
            image,
            [install_openvino_dependencies,
             bash('cd /opt/intel/openvino/samples/cpp && '
                  '/opt/intel/openvino/samples/cpp/build_samples.sh'),
             bash('omz_downloader --name alexnet --precisions FP16 '
                  '-o /root/inference_engine_cpp_samples_build/intel64/Release/'),
             bash('mo --output_dir /root/inference_engine_cpp_samples_build/intel64/Release/public '
                  '--input_model /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet/'
                  'alexnet.caffemodel'),
             bash('umask 0000 && /root/inference_engine_cpp_samples_build/intel64/Release/classification_sample_async '
                  '-m /root/inference_engine_cpp_samples_build/intel64/Release/public/alexnet.xml '
                  '-i /opt/intel/openvino/samples/scripts/car_1.bmp -d HDDL && rm -f /dev/shm/hddl_*'),
             ], self.test_classification_async_cpp_hddl.__name__, **kwargs,
        )
