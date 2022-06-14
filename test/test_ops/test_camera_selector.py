# yapf: disable
import mmcv
import numpy as np
import os

from xrmocap.ops.triangulation.builder import (
    build_point_selector, build_triangulator,
)
from xrprimer.data_structure.camera import FisheyeCameraParameter  # noqa:E501

# yapf: enable


def test_camera_error_selector():
    keypoints2d = np.load(
        os.path.join('test/data/test_ops/test_triangulation',
                     'keypoints2d.npz'))['keypoints2d']
    view_n, frame_n, keypoint_n, _ = keypoints2d.shape
    cam_param_list = []
    for kinect_index in range(view_n):
        cam_param_path = os.path.join('test/data/test_ops/test_triangulation',
                                      f'cam_{kinect_index:02d}.json')
        cam_param = FisheyeCameraParameter()
        cam_param.load(cam_param_path)
        cam_param_list.append(cam_param)
    # build a triangulator
    triangulator_config = dict(
        mmcv.Config.fromfile(
            'config/ops/triangulation/aniposelib_triangulator.py'))
    triangulator_config['camera_parameters'] = cam_param_list
    triangulator = build_triangulator(triangulator_config)
    # build a camera selector
    camera_selector = dict(
        mmcv.Config.fromfile(
            'config/ops/triangulation/camera_error_selector.py'))
    camera_selector['triangulator']['camera_parameters'] = \
        triangulator.camera_parameters
    camera_selector['target_camera_number'] = \
        len(triangulator.camera_parameters) - 1
    camera_selector = build_point_selector(camera_selector)
    # test camera inidexes
    camera_inidexes = camera_selector.get_camera_inidexes(points=keypoints2d)
    assert len(camera_inidexes) == len(triangulator.camera_parameters) - 1
    # test camera mask
    init_mask = np.ones_like(keypoints2d[..., 0:1])
    keypoints2d_backup = keypoints2d.copy()
    init_mask_backup = init_mask.copy()
    points2d_mask = camera_selector.get_selection_mask(keypoints2d, init_mask)
    assert np.all(keypoints2d_backup == keypoints2d)
    assert np.allclose(init_mask_backup, init_mask, equal_nan=True)
    assert np.all(points2d_mask.shape == init_mask.shape)


def test_slow_camera_error_selector():
    keypoints2d = np.load(
        os.path.join('test/data/test_ops/test_triangulation',
                     'keypoints2d.npz'))['keypoints2d']
    view_n, frame_n, keypoint_n, _ = keypoints2d.shape
    cam_param_list = []
    for kinect_index in range(view_n):
        cam_param_path = os.path.join('test/data/test_ops/test_triangulation',
                                      f'cam_{kinect_index:02d}.json')
        cam_param = FisheyeCameraParameter()
        cam_param.load(cam_param_path)
        cam_param_list.append(cam_param)
    # build a triangulator
    triangulator_config = dict(
        mmcv.Config.fromfile(
            'config/ops/triangulation/aniposelib_triangulator.py'))
    triangulator_config['camera_parameters'] = cam_param_list
    triangulator = build_triangulator(triangulator_config)
    # build a camera selector
    camera_selector = dict(
        mmcv.Config.fromfile(
            'config/ops/triangulation/slow_camera_error_selector.py'))
    camera_selector['triangulator']['camera_parameters'] = \
        triangulator.camera_parameters
    camera_selector['target_camera_number'] = \
        len(triangulator.camera_parameters) - 1
    camera_selector = build_point_selector(camera_selector)
    # test camera inidexes
    camera_inidexes = camera_selector.get_camera_inidexes(points=keypoints2d)
    assert len(camera_inidexes) == len(triangulator.camera_parameters) - 1
    # test camera mask
    init_mask = np.ones_like(keypoints2d[..., 0:1])
    keypoints2d_backup = keypoints2d.copy()
    init_mask_backup = init_mask.copy()
    points2d_mask = camera_selector.get_selection_mask(keypoints2d, init_mask)
    assert np.all(keypoints2d_backup == keypoints2d)
    assert np.allclose(init_mask_backup, init_mask, equal_nan=True)
    assert np.all(points2d_mask.shape == init_mask.shape)
