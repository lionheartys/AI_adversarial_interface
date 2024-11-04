## Introduction

This code achieves an interface, receiving the POST and GET then scheduling several docker containers where adversarial samples are generated.

Now it implemented to Task 10, and Docker container has not been linked yet.




## Usage
  * setting with ip and port in gunicorn.conf.py, as follows:

    workers = 5
    

> worker_class = "gevent"
    

> bind = "127.0.0.1:5901"  // ip and  port

* using run.sh to start the interface:

    chmod a+x run.sh && ./run.sh

## Debug mode
  //in the url blank:
  
  * for testing mode1 获取被测对象的数据源:
  
    http://127.0.0.1:5901/test_model

  * for testing mode2 获取内置依赖库及其版本的数据源
  
    http://127.0.0.1:5901/depn_lib

  * for testing mode3 获取被测对象的模型权重文件数量
  
    http://127.0.0.1:5901/weight_number?test_model=Vgg16

  * for testing mode4 被测对象的模型权重文件zip包下载
  
    http://127.0.0.1:5901/weight_download?test_model=Vgg16

  * for testing mode5 获取被测对象的模型权重文件列表、对抗方法列表的数据源
  
    http://127.0.0.1:5901/check_model?test_model=Vgg16


  * for testing mode6 启动对抗样本生成
    
    * leveraging curl for POST:

```shell
curl -X POST http://127.0.0.1:5901/adver_gen \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "mission_id=123&test_model=Vgg16&test_weight=weightA&test_seed=seed1&test_method=FGSM&timeout=3600"  \
--noproxy 127.0.0.1     ***if you has set proxy, this option should be added***
```

  * for testing mode7 对抗样本生成过程中数据轮询
  
    http://127.0.0.1:5901/adver_gen?mission_id=123

  * for testing mode8 停止对抗样本生成
    
```shell
curl -X POST http://127.0.0.1:5901/adver_gen_stop \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "mission_id=123" \
--noproxy 127.0.0.1    
```

* for testing mode9 生成的对抗样本zip包下载
  
    http://127.0.0.1:5901/adver_gen_download?mission_id=321

* for testing mode10 获取不同被测对象下的评估配置指标
  
    http://127.0.0.1:5901/adver_metrics?test_model=Vgg16


