# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
import os
import pathlib

import pytest

root = pathlib.Path(os.path.realpath(__name__)).parent
kwargs = {
    'mem_limit': '3g',
    'volumes': {
        root / 'tests' / 'resources' / 'python_bindings': {'bind': 'C:\\tmp\\python_bindings'},
    },
    'user': 'ContainerAdministrator',
}


@pytest.mark.windows
class TestPythonBindingsWindows:
    def test_openvino_bindings(self, tester, image):
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'python C:\\\\tmp\\\\python_bindings\\\\openvino_bindings.py',
             ],
            self.test_openvino_bindings.__name__, **kwargs,
        )

    @pytest.mark.usefixtures('_python_ngraph_required')
    def test_ngraph_bindings(self, tester, image):
        tester.test_docker_image(
            image,
            ['cmd /S /C  C:\\\\intel\\\\openvino\\\\setupvars.bat && '
             'python C:\\\\tmp\\\\python_bindings\\\\ngraph_bindings.py',
             ],
            self.test_ngraph_bindings.__name__, **kwargs,
        )
