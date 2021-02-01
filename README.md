## 0x01 概述



使用腾讯云函数+Server酱完成零组文库自动签到，效果如图：

![image-20210201111657108](https://typora-mine.oss-cn-beijing.aliyuncs.com/typora/image-20210201111657108.png)



## 0x02 使用

1. 需要填写部分如图所示：

   ![image-20210201112021822](https://typora-mine.oss-cn-beijing.aliyuncs.com/typora/image-20210201112021822.png)



2. 百度API请至此URL申请（https://console.bce.baidu.com/），ApiKey和SecretKey如图所示：

   ![image-20210201112316486](https://typora-mine.oss-cn-beijing.aliyuncs.com/typora/image-20210201112316486.png)



3. 腾讯云函数至此URL申请（https://console.cloud.tencent.com/），使用教程不赘述，直接把代码复制进入即可，最后加个定时器触发，配置完成。

   ![image-20210201112731669](https://typora-mine.oss-cn-beijing.aliyuncs.com/typora/image-20210201112731669.png)



## 0x04 使用问题

1. 如果出现超时，在函数设置里修改超时时间为最大**900**。

   ![image-20210201120625415](https://typora-mine.oss-cn-beijing.aliyuncs.com/typora/image-20210201120625415.png)

   

2. 如果出现其他问题，如Server酱无法发送信息，强烈建议勾选“**固定出口IP选项**”。

   ![image-20210201120817279](https://typora-mine.oss-cn-beijing.aliyuncs.com/typora/image-20210201120817279.png)