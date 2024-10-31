
#coding=utf-8
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"code": 1, "message": "No file part in the request"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"code": 2, "message": "No selected file"})

    target_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'testcases')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    file.save(os.path.join(target_folder, file.filename))

    file_size = os.path.getsize(os.path.join(target_folder, file.filename))

    response = {
        "code": 200,
        "message": "File uploaded successfully",
        "data": {
            "fileName": file.filename,
            "fileSize": file_size
        }
    }

    return jsonify(response)

@app.route('/scan', methods=['GET'])
def scan_files():
    fileName = request.args.get('fileName')
    dockerName = request.args.get('dockerName')

    # �~I���~L scan �~D~Z�~\�并读�~O~V�~V~G件�~F~E容
    scan_script = "../scan.sh {}".format(fileName)
    os.system(scan_script)

    # 读�~O~V��~S�~^~\�~V~G件�~F~E容
    scan_result_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scan_result')
    with open(os.path.join(scan_result_folder, 'forFunc'), 'r') as for_file:
        forFunc = for_file.read().strip().split(',')

    with open(os.path.join(scan_result_folder, 'recFunc'), 'r') as rec_file:
        recFunc = rec_file.read().strip().split(',')

    with open(os.path.join(scan_result_folder, 'scandetail'), 'r') as detail_file:  #####
        scandetail = detail_file.read().strip()                                     #####

    response = {
        "code": 200,
        "Message": "�~I��~O~O�~H~P�~J~_",
        "Data": {
            "scanResult": scandetail,
            "recFunc": recFunc,
            "forFunc": forFunc
        }
    }

    return jsonify(response)


@app.route('/execute_script', methods=['GET'])
def execute_script():
    function_list = request.args.get('function_list')
    rec_func = request.args.get('rec_func')

    # �~^~D建�~I���~L start.bash �~D~Z�~\��~Z~D�~Q�令
    execute_scirpt = "../start.sh {} {}".format(function_list,rec_func)

    # �~I���~L�~Q�令
    result = os.system(execute_scirpt)

    if result == 0:
        return jsonify({
            "code": 200,
            "message": "��~@��~K��~O��~^�~L~V�~N~X.",
            "data": {
                "expStatus": 0
            }
        })
    else:
        return jsonify({
            "code": 400,
            "message": "�~I���~L�~D~Z�~\�失败",
            "data": {
                "expStatus": 1
            }
        })

@app.route('/query_results', methods=['GET'])
def query_results():
    fileName = request.args.get('fileName')
    dockerName = request.args.get('dockerName')

    # �~\���~J级�~[���~U�~I���~L showdetail.sh �~D~Z�~\�
    os.system("../showdetail.sh {}".format(fileName))

    # ��~@�~_��~X��~P���~X�~\� fuzz_result �~V~G件夹�~O~J�~E�中�~Z~D fuzzResult �~V~G件
    if os.path.exists("../fuzz_result/fuzzResult"):
        with open("../fuzz_result/fuzzResult", 'r') as file:
            content = file.read()
            data = {
                "runTime": content.split(';')[0].split(':')[-1].strip(),
                "totalPaths": content.split(';')[1].split(':')[-1].strip(),
                "uniqCrashes": content.split(';')[2].split(':')[-1].strip(),
                "mapDensity": content.split(';')[3].split(':')[-1].strip(),
                "totalCrashes": content.split(';')[4].split(':')[-1].strip()
            }
            response = {
                "code": 200,
                "message": "�~L~V�~N~X信�~A�",
                "data": {
                    "showDetail": data,
                    "expStatus": 0
                }
            }
    else:
        response = {
            "code": 400,
            "message": "fuzzResult �~V~G件��~M��~X�~\�",
            "data": {}
        }

    return jsonify(response)


@app.route('/query_results', methods=['GET'])
def query_results():
    fileName = request.args.get('fileName')
    dockerName = request.args.get('dockerName')

    # �~\���~J级�~[���~U�~I���~L showdetail.sh �~D~Z�~\�
    os.system("../showdetail.sh {}".format(fileName))

    # ��~@�~_��~X��~P���~X�~\� fuzz_result �~V~G件夹�~O~J�~E�中�~Z~D fuzzResult �~V~G件
    if os.path.exists("../fuzz_result/fuzzResult"):
        with open("../fuzz_result/fuzzResult", 'r') as file:
            content = file.read()
            data = {
                "runTime": content.split(';')[0].split(':')[-1].strip(),
                "totalPaths": content.split(';')[1].split(':')[-1].strip(),
                "uniqCrashes": content.split(';')[2].split(':')[-1].strip(),
                "mapDensity": content.split(';')[3].split(':')[-1].strip(),
                "totalCrashes": content.split(';')[4].split(':')[-1].strip()
            }
            response = {
                "code": 200,
                "message": "�~L~V�~N~X信�~A�",
                "data": {
                    "showDetail": data,
                    "expStatus": 0
                }
            }
    else:
        response = {
            "code": 400,
            "message": "fuzzResult �~V~G件��~M��~X�~\�",
            "data": {}
        }

    return jsonify(response)


@app.route('/stop_script', methods=['GET'])
def stop_script():
    fileName = request.args.get('fileName')
    dockerName = request.args.get('dockerName')

    # �~I���~L stop.sh �~D~Z�~\��~]��~I~S��~@ Ubuntu ��~H端并�~X�示 fileName �~Z~D�~@�
    stop_script = "../stop.sh {}".format(fileName)
    result = os.system(stop_script)

    # ��~T�~[~^ JSON �~U��~M�
    if result == 0:
        return jsonify({
            "code": 200,
        "message": "��~O��~^�~L~V�~N~X已�~A~\止",
        "data": {
            "expStatus": 1
        }
        })
    else:
        return jsonify({
            "code": 400,
            "message": "�~I���~L�~D~Z�~\�失败",
            "data": {
                "expStatus": 2
            }
        })

if __name__ == "__main__":
    app.run(debug=True)

