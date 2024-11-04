
#coding=utf-8
from flask import Flask, request, jsonify
import os
from utils import *
from Misson_class import *

app = Flask(__name__)


@app.route('/adver_metrics', methods=['GET'])
def adver_metrics():
    test_model = request.args.get('test_model')
    model_dict = init_read_yaml_for_model()

    if "adver_metrics" in model_dict[test_model].keys():
        return jsonify({
            "code": 200,
            "message": "模型的评估指标",
            "data": model_dict[test_model]["adver_metrics"],
        })
    else:
        return jsonify({
            "code": 400,
            "message": "模型不对",
            "data": {}
        })

@app.route('/adver_gen_download', methods=['GET'])
def adver_gen_download():
    mission_id = request.args.get('mission_id')

    if mission_id:
        return jsonify({
            "code": 200,
            "message": "生成的对抗样本zip包下载",
             "zipAddr": "xxxx",
        })
    else :
        return jsonify({
            "code": 400,
            "message": "任务ID未识别",
            "zipAddr": {}
        })


@app.route('/adver_gen_stop', methods=['POST'])
def adver_gen_stop():
    print("Received POST request")
    mission_id = request.form.get('mission_id', default=None, type=str)
    mission_manager = MissionManager('Adver_gen_missions_DBSM.csv')

    if mission_id not in mission_manager.missions.keys():
        return jsonify({
            "code": 400,
            "message": "任务不存在，id有误",
            "data": {"status": 2},
        })
    else:
        mission = mission_manager.missions[mission_id]
        mission.update_status(1)
        mission_manager.add_or_update_mission(mission)
        return jsonify({
            "code": 200,
            "message": "任务已停止",
            "data": {"status": 1},
        })


@app.route('/adver_gen', methods=['GET'])
def adver_gen_get():
    mission_id = request.args.get('mission_id')

    mission_manager = MissionManager('Adver_gen_missions_DBSM.csv')
    if mission_id not in mission_manager.missions.keys():
        return jsonify({
            "code": 400,
            "message": "任务不存在，id有误",
            "data": {"status": 2},
        })
    else:
        return jsonify({
            "code": 200,
            "message": "任务执行中",
            "data": {
                "dataNum": 2000,
                "status": mission_manager.missions[mission_id].mission_status},
        })


@app.route('/adver_gen', methods=['POST'])
def adver_gen():
    print("Received POST request")
    mission_id = request.form.get('mission_id', default=None, type=str)
    test_model = request.form.get('test_model', default=None, type=str)
    test_weight = request.form.get('test_weight', default=None, type=str)
    test_seed = request.form.get('test_seed', default=None, type=str)
    test_method = request.form.get('test_method', default=None, type=str)
    timeout = request.form.get('timeout', default=None, type=int)

    mission_manager = MissionManager('Adver_gen_missions_DBSM.csv')

    if mission_id in mission_manager.missions.keys():   ###  if same mission id is executed twice, will report error
        return jsonify({
            "code": 400,
            "message": "该任务已存在",
            "data": {"status": 2},
        })

    if all([mission_id, test_model, test_weight, test_seed, test_method, timeout]):
        mission_status = 2
        mission = Mission(mission_id, test_model, test_weight, test_seed, test_method, timeout, mission_status)
        mission_manager.add_or_update_mission(mission)

        return jsonify({
            "code": 200,
            "message": "任务已开始执行",
            "data": {"status": 1},
        })
    else:
        return jsonify({
            "code": 400,
            "message": "POST参数有误",
            "data": {"status": 2},
        })

@app.route('/check_model', methods=['GET'])
def check_model():
    test_model = request.args.get('test_model')

    model_dict = init_read_yaml_for_model_duplicate()

    if model_dict[test_model]['download_addr']:
        return jsonify({
            "code": 200,
            "message": "模型权重文件、对抗方法列表",
             "weightList": model_dict[test_model]['weight_name'],
            "methodList": model_dict[test_model]['test_method']
        })
    else :
        return jsonify({
            "code": 400,
            "message": "模型权重文件、对抗方法列表收集失败",
            "weightList": {},
            "methodList": {}
        })

@app.route('/weight_download', methods=['GET'])
def weight_download():
    test_model = request.args.get('test_model')

    model_dict = init_read_yaml_for_model_duplicate()

    if isinstance(model_dict[test_model]['download_addr'], list):
        return jsonify({
            "code": 200,
            "message": "模型权重文件下载, 多个地址",
             "weightDown": model_dict[test_model]['download_addr']
        })

    elif isinstance(model_dict[test_model]['download_addr'], str):
        return jsonify({
            "code": 200,
            "message": "模型权重文件下载",
             "weightDown": model_dict[test_model]['download_addr']
        })
    else :
        return jsonify({
            "code": 400,
            "message": "模型权重文件下载类型不对",
            "weightDown": {}
        })


@app.route('/weight_number', methods=['GET'])
def weight_number():
    test_model = request.args.get('test_model')

    model_dict = init_read_yaml_for_model_duplicate()

    if isinstance(model_dict[test_model]['weight_number'], int):
        return jsonify({
            "code": 200,
            "message": "模型权重文件数量",
             "weightNum": model_dict[test_model]['weight_number']
        })

    elif isinstance(model_dict[test_model]['weight_number'], str):
        return jsonify({
            "code": 400,
            "message": "请换个模型，这个没有权重",
             "weightNum": model_dict[test_model]['weight_number']
        })
    else :
        return jsonify({
            "code": 400,
            "message": "模型权重文件数量类型不是int, please chech codes",
            "weightNum": {}
        })


@app.route('/depn_lib', methods=['GET'])
def depn_lib():
    model_dict = init_read_yaml_for_model()

    data = [{"targetName": key, "versionList": \
        [f"{kk}-{str(vv)}" for kk, vv in model_dict[key]["dependents"].items()]} for key in model_dict.keys()]

    if isinstance(data, list):
        return jsonify({
            "code": 200,
            "message": "内置依赖库及其版本信息",
            "data": data
        })
    else:
        return jsonify({
            "code": 400,
            "message": "内置依赖库获取失败",
            "data": {}
        })


@app.route('/test_model', methods=['GET'])
def test_model():
    model_dict = init_read_yaml_for_model()
    data = list(model_dict.keys())

    if isinstance(data, list):
        return jsonify({
        "code": 200,
        "message": "被测对象的详细信息",
        "data": data
        })
    else:
        return jsonify({
            "code": 400,
            "message": "未能读取到模型列表",
            "data": {}
        })

if __name__ == "__main__":
    app.run(debug=True)

