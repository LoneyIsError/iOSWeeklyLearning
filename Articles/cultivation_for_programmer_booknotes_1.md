# 《程序员的自我修养（链接、装载与库）》学习笔记一（稳固而知新）
![封面](https://cdn.zhangferry.com/Images/%E7%A7%8B%E5%A4%A9%E5%8D%A1%E9%80%9A%E6%89%8B%E7%BB%98%E9%A3%8E%E7%AB%96%E7%89%88%E6%8F%92%E7%94%BB__2022-11-07+16_45_20.png)

[《程序员的自我修养 - 链接、装载与库》](https://book.douban.com/subject/3652388/ "《程序员的自我修养 - 链接、装载与库》")这本书，主要是介绍了系统软件的一些运行机制、原理。在不同的系统平台上，一个应用程序在编译、链接、运行发生的各种事项，并对此进行了深入的剖析。本书主要分成四个大的章节，温故而知新、静态链接、装载与动态链接、库与运行库：

|  温故而知新  |     静态链接     |     装载与动态链接     |   库与运行库   |
| :----------: | :--------------: | :--------------------: | :------------: |
|  计算机发展  |    编译和链接    | 可执行文件的装载与进程 |      内存      |
| 软件体系结构 | 目标文件里有什么 |        动态链接        |     运行库     |
|   操作系统   |     静态链接     |   Linux 共享库的组织   | 系统调用与 API |
|  内存、线程  | Windows PE/COFF  |  Windows 下的动态链接  |   运行库实现   |

在这书里有一句话，是之前认识的一个研发长者经常挂在嘴边的，今天在书中看到了感触颇多：

> 经常听很多人谈起，IT 技术日新月异，其实真正核心的东西数十年都没怎么变化，变化的仅仅是它们外在的表现，大体也是换汤不换药吧。

本书的作者介绍之所以想写这本书，其实主要也是因为不满足于技术的表面，想探索问题的根源。就像上面写的，技术发展日新月异，但是核心的东西却是相对稳定不变的，那么对于从事软件开发的工程师，研究人员，学习这些底层的知识就很有必要了，很多技术都是相通的，认识了底层才更能看清事情的表象，达到触类旁通的效果，毕竟只会写代码不是好程序员，这也是我想学习这本书的原因之一。

除此之外，这本书被大家评价为国人难得写的比较不错的一本计算机技术书籍，并且成为很多大厂人员的必读书籍，肯定是有其魅力所在的，那么是时候认真阅读一下了。

## 温故而知新

本书的第一章主要分为五个部分，除了第一部分主要是抛出几个问题让大家一起思考之外，剩下部分分别为计算机的发展，软件体系结构，内存和线程。具体知识点分布如图所示：

![](https://cdn.zhangferry.com/Images/WX20221113-184435@2x.png)

### Hello World引发的思考

```c
#include <stdio.h>

int main() {
    printf("Hello World\n");
    return 0;
}

```

针对这小段代码，本书抛出了一些问题。

* 为什么程序编译了才能运行？
* 编译器将 C 代码转化为机器码，做了什么？
* 编译出的可执行文件中有什么，存放机制是什么？
* ....

关于上述问题，本书会从基本的编译、链接开始讲解，然后到装载程序、动态链接等。

### 计算机基本结构以及CPU的发展

#### 结构

计算机基本结构：**CPU、内存、I/O 控制芯片**，如下图：

<img src="https://cdn.zhangferry.com/Images/WX20221112-175653@2x.png" width = "650"/>

#### CPU 的发展史

1. 早期 CPU 的核心频率很低，几乎等于内存频率，每个设备都会有一个 I/O 控制器，链接在一条总线（Bus）上。
2. 随着 CPU 核心频率的提升，内存访问速度低于 CPU，于是增加了处理高速 I/O 的北桥芯片和处理低速 I/O 的南桥芯片。
3. CPU 速度达到极限后，又增加了多核处理器 SMP。

### 软件体系结构

下图为计算机的软件体系结构分层:

<img src="https://cdn.zhangferry.com/Images/%E8%AF%95%E8%AF%95.png" width = "650"/>

1. 计算机软件体系结构是分层的，层与层之间通信的协议，称之为接口。
  1. 开发工具与应用程序都使用操作系统的**应用程序编程接口**。
  2. 运行库使用操作系统的**系统调用接口**。
2. 接口需精心设计，尽量保持稳定，基于接口，具体实现层可以被任意替换。
3. 中间层作为下面层级的包装和扩展，中间层的存在，保证了软硬件的相对独立。
4. 操作系统提供抽象接口，管理软件、硬件资源。操作系统内核作为硬件接口的使用者，需定制硬件规格，硬件逐渐被抽象成一套接口，交给厂商，厂商写各自的驱动程序，硬件交互细节交给操作系统（驱动），程序员无需和硬件打交道。

#### 分层
分层设计的思想，其实渗透在计算机的各个领域。其中有我们最熟悉的 OSI 七层网络模型，它从低到高分别是：物理层、数据链路层、网络层、传输层、会话层、表示层和应用层。参考计算机的软件体系结构，OSI 网络模型同样是通过制定层层的通信协议，界定各个分层的具体责任和义务。

<table>
    <tr>
        <td>OSI七层网络模型</td> 
        <td>TCP/IP四层概念模型</td> 
        <td>对应网络协议</td> 
   </tr>
   <tr>
        <td>应用层</td> 
        <td rowspan="3">应用层</td> 
        <td>HTTP、TFTP、FTP、NFS、WAIS、SMTP</td>    
   </tr>
   <tr>
        <td>表示层</td> 
        <td>Telnet、Riogin、SNMP、Gopher</td> 
   </tr>
    <tr>
        <td>会话层</td> 
        <td >SMTP、DNS</td>  
    </tr>
    <tr>
        <td >传输层</td> 
        <td >传输层</td>
        <td >TCP、UDP</td> 
    </tr>
     <tr>
        <td >网络层</td> 
        <td >网络层</td>
        <td >IP、ICMP、ARP、RARP、AKP、UUCP</td> 
    </tr>
     <tr>
        <td >数据链路层</td> 
        <td rowspan="2">数据链路层</td> 
        <td >FDDI、Ethernet、Arpanet、PDN、SLIP、PPP</td> 
    </tr>
     <tr>
        <td >物理层</td> 
        <td >IEEE 802.1A、IEEE 802.2 到 IEEE 802.11</td> 
    </tr>
</table>
那么为什么在架构设计的时候，采用分层设计的实现方案呢？

之所以要设计分层，主要有以下几点考虑：

1. 降低复杂度，上层不需要关注下层细节。
2. 提高灵活性，可以灵活替换某层的实现。
3. 减小耦合度，将层次间的依赖减到最低。
4. 有利于重用，同一层次可以有多种用途。
5. 有利于标准化。

#### 中间层
除了分层设计，中间层的设计，也是非常巧妙的存在。

在计算机软件体系结构中，中间层作为下面层级的包装和扩展，中间层的存在，保证了软硬件的相对独立。
中间层的强大之处在 LLVM 设计的过程中也深有体现。

首先解释下 LLVM：

LLVM 是构架编译器（compiler）的框架系统，以 C++ 编写而成，用于优化以任意程序语言编写的程序的编译时间（compile-time）、链接时间（link-time）、运行时间（run-time）以及空闲时间（idle-time），对开发者保持开放，并兼容已有脚本。

LLVM 的大体结构设计如下图：
![](https://cdn.zhangferry.com/Images/WX20221107-232225@2x.png)

它的设计主要可以分为编译器前端（Frontend）、优化器（Optimizer）、后端和代码生成器（Backend And CodeGenerator）。

笔者理解优化器（Optimizer）不仅仅作为编译过程中的一道工序（做各种优化并且改善代码的运行时间，减少冗余计算），优化器还作为 LLVM 设计最为精妙的地方--`中间层`。

为什么这么说呢？

前端语法种类繁多，后端硬件架构种类繁多，而正是中间层的存在，使得 LLVM 的架构即可以为各种语言独立编写前端，也可以为任意硬件架构编写后端，实现了开发语言和硬件架构之间相对独立，这才是其真正的强大之处。

#### 类似软件的设计原则的体现

虽说是大的软件体系的结构设计，但是也能让笔者感触到一些软件设计原则的体现，毕竟万物皆对象，而面向对象设计原则如下：

|   设计原则名称    |                     简单定义                     |
| :---------------: | :----------------------------------------------: |
|     开闭原则      |              对扩展开放，对修改关闭              |
|   单一职责原则    |       一个类只负责一个功能领域中的相应职责       |
|   里氏替换原则    |  所有引用基类的地方必须能透明地使用其子类的对象  |
|   依赖倒置原则    |          依赖于抽象，不能依赖于具体实现          |
|   接口隔离原则    |      类之间的依赖关系应该建立在最小的接口上      |
| 合成/聚合复用原则 | 尽量使用合成/聚合，而不是通过继承达到复用的目的  |
|    迪米特法则     | 一个软件实体应当尽可能少的与其他实体发生相互作用 |

感受到了哪些设计原则？这列举一二，当然应该还会有更多。

1. 单一职责
    分层设计，每层只负责特定的职责，拥有清晰的职责范围。
2. 单一职责
    层与层之间交互应该依赖抽象，任何满足每层协议的实体，都可以进行层的替换。
3. 开闭原则
    采用类似工厂设计原则，增加一种硬件类型，仅需要增加一种符合硬件规格厂商即可。

**总结：我们进行日常软件架构设计的时候，其实也可以参考计算机软件设计的一些思想，做一些合适的分层，制定层与层之间的协议，制定合适的中间层。**

### 内存
早期内存采用扇形内存分区，磁盘中所有的扇区从0开始编号，直到最后一个扇区，编号为逻辑扇区号，设备会将逻辑扇区号，转换成真实的盘面、磁道位置。

#### 早期程序直接运行在物理内存，存在的问题
1. 地址空间`不隔离`，一个程序内容容易被另一个程序修改。

2. 内存使用`效率低`，使用中的内存需要等到释放了，才能继续被使用。

3. 程序运行的地址`不固定`，程序重新装载时，内存地址变化了。

#### 虚拟地址&物理地址

为了解决地址空间`不隔离`的问题，引入了虚拟地址的概念，于是地址就分为了两种，虚拟地址空间和物理地址空间。

MMU是内存管理单元，有时也称作分页内存管理单元，MMU在操作系统的控制下负责将虚拟内存实际翻译成物理内存，其与CPU以及物理内存的关系如下图：

<img src="https://cdn.zhangferry.com/Images/WX20221112-133253@2x.png" width = "600"/>

1. 物理地址空间是由地址总线条数决定的。
2. 虚拟地址是想象出来的，每个进程都拥有独立的虚拟空间，这样做到了进程的地址隔离。
3. 将一段程序所需要的虚拟空间，映射到某个实际的物理地址空间，映射函数由软件完成，实际转换由硬件完成。


#### 分段和分页

仅仅增加虚拟地址只能解决地址空间不隔离的问题，剩下两个问题还没解决，于是又引入了分段和分页。

1. 分段的基本思路是把一段与程序所需要的内存空间大小的虚拟空间映射到某个地址空间，映射关系如下图所示，通过使用分段，可以解决不隔离和不固定的问题，因为程序A和程序B被映射到了两块不同的物理空间。

   <img src="https://cdn.zhangferry.com/Images/WX20221112-180320@2x.png" width = "570"/>

2. 但是分段内存使用效率低下，内存映射以程序为单位，如果内存不足，被换出的是整个程序，其实程序内的很多数据，都不会被频繁用到，没必要被一起移除内存。

3. 分页就是将地址空间分为固定大小的页，进程的虚拟地址空间按页分隔，不常用的放入磁盘，用到时取出来即可，内存使用效率低下的问题得到了解决。

   <img src="https://cdn.zhangferry.com/Images/WX20221112-180013@2x.png" width = "600"/>

#### 内存共享的实现机制
虚拟空间页称之为虚拟页，物理内存的页为物理页，磁盘中的页为磁盘页，不同虚拟页被同时映射到同一个物理页，即可实现内存共享。

#### Page Fault
虚拟页不在内存中，当需要用到时，就会捕获 Page Fault。

对于 iOS 开发来说，虚拟内存也是通过分页管理的，当访问到某些数据并没有加载到内存时，操作系统就会阻塞当前线程，新加载一页到物理内存，并且将虚拟内存与之对应，这个阻塞的过程就叫做缺页中断，App 启动的时候 Page Fault次数多了会影响启动速度，而我们优化启动速的方式之一就是通过二进制重排，减少 Page Fault 的次数。

<div align=center><img src="https://cdn.zhangferry.com/Images/WX20221112-185849@2x.png" width = "670"/>
当 App 的启动过程中如果需要启动符号1、启动符号2、启动符号3、启动符号4，那么 page1，page2，page3，page4 就都需要加载到内存中。

<div align=center><img src="https://cdn.zhangferry.com/Images/WX20221112-185930@2x.png" width = "670"/>

而我们可以做的就是通过二进制的重排，将启动符号1、启动符号2、启动符号3、启动符号4放到了同一页，那么只需要 page1加载到内存即可。大概的优化步骤：

> 通过 Clang 插桩的方式找到 App 启动时，都加载了哪些符号，尽可能的将启动时用到的符号，通过自定义 Order File 放到同一个 启动时加载的 Page 当中，从而减少 Page Fault 的发生次数。

### 线程
线程与进程的区别在于，进程是操作系统分配资源的最小单位，线程是程序执行的最小单位。
#### 线程一些概念
1. 线程称之为轻量级进程，有线程 ID，当前指令指针 PC，寄存器，堆栈组成，线程是系统进行调度的最小单位。
2. 各个线程共享程序的内存空间（代码段、数据段、堆），和一些进程级的资源（程序员角度：全局变量、堆、函数里的静态变量、代码）。
3. 线程拥有私有的空间，栈、线程局部存储、寄存器（程序员角度：局部变量、函数参数）。
4. 多处理器的线程并发才是真正并发，单个处理器的线程并发只不过是时间片轮流，调度。
5. 线程至少三种状态：运行（时间片当中）、就绪（离开运行状态）、等待（时间片结束）。
6. 线程调度分为优先级调度（容易出现饿死）和轮转发调度。
7. Linux 线程相关的操作通过 pthread 库实现。

#### 线程安全
多线程程序处于一个多变的环境当中，可访问的全局变量和堆数据随时都可能被其他的线程改变，于是产生了原子操作和锁。

1. 原子操作 
> 1. ++操作不是原子操作（编译为汇编代码之后，不止一条指令）因为需要经历 ① 读取值到寄存器，② 值+1 ③ 将值写会寄存器。
> 2. 复杂场景，原子操作就不满足了，需要使用锁，实现同步。

2. 锁
> 实现数据访问的原子化，即一个线程未访问结束，另一个线程不能访问，访问数据时获取锁，访问结束释放锁，锁已经占用的时候，获取锁线程就会进行等待，直到锁资源可以重用。

* `二元信号量`，有两个状态，占用和非占用，适合只能被为一个线程独占访问的资源。
* `多元信号量（Semaphore）`，设置一个初始值 N，可实现 N 个线程并发访问。
* `互斥量`，类似二元信号量，二元信号量可以被其他线程获取到释放，但是互斥量要求哪个线程获取，哪个线程释放。
* `临界区`，区别于互斥量和信号量，互斥量和信号量在其他进程是可见的，但是临界区的范围仅仅限于本进程。
* `读写锁`，对于读取频繁但是偶尔写入的时候，使用信号量和互斥锁效率比较低，读写锁有共享状态和独占状态。

下图为读写锁的几种状态：

| 读写锁状态 | 已共享方式读取 | 以独占方式读取 |
| :----: | :----: | :----: |
| 自由 | 成功 | 成功 |
| 共享 | 成功 | 等待 |
| 独占 | 等待 | 等待 |

表中读写锁具体状态解析如下：
* 锁自由状态时，任何方式获取锁都可以获取成功。
* 共享状态下，共享方式获取可成功，独占方式获取不可成功。
* 独占状态下，共享方式获取、独占方式获取都不可成功 。
* 写操作作为独占状态，读操作作为共享状态，读读并发，不用等待，读写互斥，写写互斥。

##### 多线程可放心使用的函数之-可重入函数

> 满足如下条件的函数即为可重入函数

1. 不使用任何（局部）静态或全局的非 const 变量。
2. 不返回任何 （局部）静态或全局的非 const 变量的指针。
3. 仅依赖于调用方提供的参数。
4. 不依赖任何单个资源的锁（mutex 等）。
5. 不调用任何不可重入的函数。
6. 可重入是并发安全的强力保障，一个可重入的函数可以在多线程环境下放心使用。

##### 加了锁就安全了吗？

作者给我们举了一种情况：

```c++
x = 0;
// Thread1中
lock();
x++;
unlock();
 
// Thread2中
lock();
x++;
unlock();
```

上文已经介绍了 ++ 操作并非原子操作，编译器为了提高 x 的 访问速度，需要把  x  的值放入某个寄存器里面。

++ 需要经历 ① 读取值到寄存器，② 值+1 ③ 将值写会寄存器三步。

那么就可能出现这种情况：

1. Thread1读取 x 的值到寄存器 R1（此时 R1 = 0）。
2. R1 ++，此时 Thread2紧接着还要进行访问，但是 Thread1还没有将 R1值写回 x。
3. Thread2读取 x 的值到寄存器 R2（此时 R2 = 0）。
4. Thread2执行 R2 ++。
5. 这时 Thread1将 R1 写回x（**问题就来了，此时 R1 = 1，那么就出错了**）。

还有就是，CPU 发展出了动态调度的功能，在执行程序的时候，为了提高效率，有可能会交换指令的顺序，同样编译器在进行优化的时候，也是可能出现为了提高效率而交换毫不相干的两条相邻指令的顺序。

我们可以使用 volatile 关键字来阻止编译器为了提高速度将一个变量缓存到寄存器而不写回，也可阻止编译器调整操作 volatile 变量的指令顺序，但是 volatile 仅仅能够阻止编译器调整顺便，CPU 的动态交换顺序却没有办法阻止。

这里有个典型的例子，是关于单例模式的：

```c++
volatile T* pInst = 0;
T* GetInstance {
    if (pInst == NULL) {
        lock();
        if (pInst == NULL)
            pInst = new T;
        unlock();
    }
    return pInst;
}
```

这是单例模式 double-check 的案例，其中双重 if 可以令 lock 的开销降到最低，但是上面的代码其实是存在问题的，而问题就是来自于 CPU 的乱序执行。

 `pInst = new T` 一共会分为三步：

1、分配内存

2、调用构造函数 

3、将内存地址的值赋值给 pInst。

在这三步中 2、3 可能会被 CPU 颠倒顺序，那么就会出现这种情况：

`pInst` 已经不是 NULL 了，但是还没有构造完毕，这时候另一个线程调用单例方法，发现 `pInst` 不为 NULL，就会将尚未构造完成的对象地址返回，这时候类就有可能产生异常。

为解决这个问题，我们可以使用 barrier 指令，来阻止 CPU 将该指令之前的指令交换到 barrier 之后， POWERPC 体系结构使用 barrier 优化后的单例方法如下：

```c++
#define barrier() __asm__ volatile ("lwsync")
volatile T* pInst = 0;
T* GetInstance {
    if (!pInst) {
        lock();
        if (!pInst) {
           T* temp = new T;
           barrier();
           pInst = temp;
        } 
        unlock();
    }  
    return pInst;
}
```

#### 线程使用模型

1. 一对一模型

    一个用户使用的线程就唯一对应一个内核使用的线程，这样用户线程就有了和内核线程一致的优点。这种情况下，才是真正的并发，如下图：

    <img src="https://cdn.zhangferry.com/Images/WX20221112-190535@2x.png" width = "620"/>

    * 优点：一个线程受阻时，其他的线程不会受到影响。
    * 缺点1：内核线程数量的限制，导致用户线程受到限制。
    * 缺点2：内核线程调度时，上下文开销较大，导致用户的执行效率降低。

2. 多对一模型

    多个用户线程映射一个内核线程，如下图：

    <img src="https://cdn.zhangferry.com/Images/WX20221112-181704@2x.png" width = "560"/>

    * 优点：高效的上下文切换和几乎无限制的线程数量。
    * 缺点1：一个线程阻塞，其他线程都将无法执行。
    * 缺点2：多处理器不会对，对多对一模型性能没有明显帮助。

3. 多对多模型

    将多个用户线程映射到不止一个的内核线程，如下图：

    <img src="https://cdn.zhangferry.com/Images/WX20221112-181741@2x.png" width = "550"/>

    * 优点1：一个线程的阻塞不会导致所有线程阻塞。
    * 优点2：多对多模型，线程的数量没有什么限制。
    * 优点3：多处理器系统上，多对多模型性能有提升。
    * 缺点：实现较为困难。



























