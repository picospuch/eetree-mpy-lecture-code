<p align="center"><img style="float: right;" src="https://wechatapppro-1252524126.file.myqcloud.com/appU1KFqMYL7963/image/b_u_5def130d79889_zsLefqy6/kuqqho7j0rc7.png" /></p>

****本代码库是硬禾学堂《嵌入式系统入门》课程的支持代码仓库，这里的例程和支持文件针对课程配套的训练板开发，适用于硬禾学堂MicroPython扩展训练板。****


## 参考链接

-   MicroPython扩展学习板的硬件信息
    <https://www.eetree.cn/project/detail/584>

-   一些有趣的案例
    <https://www.eetree.cn/wiki/pico_micropython>


# MicroPython扩展学习板点灯（上手教程）

<p align="center"><img style="float: right;" src="https://wechatapppro-1252524126.file.myqcloud.com/appU1KFqMYL7963/image/b_u_5def130d79889_zsLefqy6/kuqqmkr30ewl.png" /></p>


# 目录结构

    ./mpy-lecture-code/
    |-- app                # 应用程序，一个py文件代表一个应用程序
    |-- bsp                # 板级支持包，在运行应用程序之前，需要将这里的文件上传pico根目录或者lib目录
    |-- help               # 帮助文件，micropython html版本帮助文件
    |-- makefile           # make构建脚本，可以用这个脚本管理代码库，完成开发流程
    |-- README.md          # 说明文件
    |-- res                # 资源文件，部分应用程序也会依赖于这里的资源（图片，声音等），需要将需要的文件上传到pico根目录或者lib目录
    `-- ria                # 测试应用程序，这里面存放为快速实验编写的应用程序，成熟后可能会放到app中


# Jupyter笔记

-   01 关于MicroPython
-   02 嵌入式系统基本概念及学习
-   03 点亮一颗LED
-   04 用输入按键控制LED的状态
-   05 交通灯的控制
-   06 测量反应时间的游戏 - 中断和服务
-   07 播放"我和我的祖国" - PWM的产生及应用
-   08 模拟信号的转换和数据处理 - ADC
-   09 将温度传到上位机 - UART通信
-   10 将字符和波形显示在OLED上 - SPI总线
-   11 用姿态传感器制作一个水平仪 - I2C总线
-   12 用麦克风制作一个音频示波器/频谱仪
-   13 PIO点亮WS2812B灯串
-   14 PIO/DMA产生任意信号波形
-   15 综合 - 制作一个定时报时/RGB显示的时钟

<p align="center"><img style="float: right;" src="http://wechatapppro-1252524126.file.myqcloud.com/appU1KFqMYL7963/image/44d838b990171176e5c55c2b73894db7.png" /></p>

