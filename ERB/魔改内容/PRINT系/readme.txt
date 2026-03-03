PRINT是游戏中最重要的交互流程，
为此，历史上多个era游戏及其变体都开发了各自的PRINT工具。为避免重复造轮子和引导创作者，将这些函数全部归纳在此。
1：打印与交互(Print and Input)
  PRINT系函数的封装，PRINT系与INPUT交互的封装。  
2：排版与字符串处理(String Layout & Format)
  式中函数，不产生任何屏幕输出，仅负责加工字符串。
3：UI 组件与制表 (UI Components & Tables)
  由模块1、模块2组成的拼装而成的高级静态 UI 组件，及其辅助颜色模块。
4：视觉特效与动画 (Visual_Effects_&_Animations)
  需要考虑屏幕刷新机能的动态效果渲染。
5：HTML渲染 (HTML_PRINT Components)
  专为 HTML_PRINT服务的标签拼装与解析。
6：高级封装
  高级的类事件封装或者其位置索引。

以下是概述：
;==============================================================================
; 3：UI 组件与制表 (UI Components & Tables)
;==============================================================================

; ────────────────────────────────────────────────────────────────
; 模块分类与主要函数一览
; ────────────────────────────────────────────────────────────────
;
; 1. @基础颜色转换与提取
;    ├─ RGB_TO_HEX / HEX_R / HEX_G / HEX_B          → RGB ↔ 0xRRGGBB 互转
;    ├─ HEX_TO_RGB / HEX_TO_RGB_F                   → HEX 拆成 R,G,B
;    └─ HEX_TO_HTML_COLOR / HEX_TO_STR              → 转为 #RRGGBB 字符串（HTML 用）
;
; 2. @HSV 颜色系统（核心渐变基础）
;    ├─ RGB_TO_HSV / HSV_TO_RGB                     → RGB ↔ HSV (打包格式：H<<16 | S<<8 | V)
;    └─ COLOR_LERP_HSV                              → HSV 空间线性插值（最自然渐变）
;
; 3. @颜色混合与 Alpha 处理
;    ├─ MIX_COLOR                                   → 两色按权重混合
;    ├─ CALC_ALPHA_COLOR                            → 带透明度的前景+背景融合
;    └─ SET_ALPHA_COLOR / RESET_ALPHA_COLOR         → 旧版兼容：设置/重置带 Alpha 颜色
;
; 4. @字符式进度条（HTML <font> 实现，轻量、易混排）
;    ├─ QOL_HTML_BARSTR                             → 核心生成器：支持 HSV 逐字符渐变、自定义字符
;    ├─ PRINT_COLORBAR                              → 直接打印版（最常用）
;    ├─ HTML_COLORBAR                               → 返回字符串版（兼容旧接口）
;    ├─ BW_BAR                                      → 黑白/灰阶简洁版
;    └─ COLOR_BAR                                   → 带彩虹尾渐变的专用条（RGB 参数接口，已内部转 HSV）
;
; 5. @像素级矩形进度条（<shape> 实现，高精度、现代感）
;    ├─ HTML_RECT_BAR                               → 核心：像素级 HSV 渐变矩形条
;    ├─ PRINT_RATE_BAR / PRINT_RATE_BAR_EX          → 高精度分段条：支持双层、超限、间隙、对齐、粗细调节
;    └─ LAYER_RECTBAR                               → 旧接口兼容层，重定向到 HTML_RECT_BAR
;
; 6. @装饰性 UI 元素
;    └─ COLOR_LINE                                  → 彩色渐变分割线（正向淡出 / 反向光晕）
;
; 7. @颜色选择器（渲染与交互的高级HTML组件）
;    ├─ HTML_PRINT_RGB_SLIDER                       → RGB 三通道滑块（按钮式）
;    └─ HTML_PRINT_HSB_SLIDER                       → HSB 三通道滑块（更符合人眼感知）
;
; 8. @辅助工具
;    └─ HTML_STRLENS                                → 计算含 <shape> 的 HTML 字符串实际显示长度（半角单位）
;
调查发现函数库一共有如下的颜色底层功能，各自为战，参数各不统一：
1. @高手糊零张派：
@HEXTORGB 返回类似 "255//0//0" 的字符串，@RGBTOHEX 接收此类字符串转为 16 进制。极度低效。
动态特效组件FULLCUTIN内高频调用。
2. @离散型工业派：
@RGB_TO_H / RGB_TO_S / RGB_TO_V，必须分三次调用才能拿到 HSV，每次调用都要重复计算 RGB 转 HSV 的过程。
@HSV_TO_RGB(H, S, V)，强制要求传入三个独立的参数。参数范围是360，100，100
@COLOR_LINE渐变分割线组件使用。
4. @密集型工业派：
@CALC_CALOR_HSB，强制要求传入三个独立的参数的HSB转换函数，参数范围是359，255，255
@CALC_CALOR，明度计算，计算RGB偏移色。
@SET_CHANGING_COLOR呼吸灯配色函数使用，但是用的是RGB线性插值。
可以说，基本所有的渐变色UI组件都在用RGB线性插值，没有用工具函数就是在组件内手算偏移值。
5. @奸奇派：
烙印系统搬运的一套库，全小写函数，功能丰富
@alpha_color，明度计算，根据 0-255 的 Alpha 值将颜色与背景色混合，用@color_mix插值实现。
@color_mix，两组RGB值加权混色。
@hex_to_rgb，利用 RETURN  RESULT 数组来实现一个函数返回 R,G,B 三个值。可以用，但是没有在用。
@hex_to_str，HTML使用的字符串转换，把数字转换成形如 FF0000的字符串。实现极度低效。格式与比反R的HTML工具库的HTMLCOLOR少一个"#"。不同的剧本或系统参考的函数不同，导致混乱。

现在的方案如下，函数间传递的颜色都是一个整数参数(HEX)
基础颜色转换与提取
├─ RGB_TO_HEX / HEX_R / HEX_G / HEX_B          → RGB ↔ 0xRRGGBB 互转
├─ HEX_TO_RGB / HEX_TO_RGB_F                   → HEX 拆成 R,G,B
└─ HEX_TO_HTML_COLOR / HEX_TO_STR              → 转为 #RRGGBB 字符串（HTML 用）

HSV 与 渐变
├─ RGB_TO_HSV / HSV_TO_RGB                     → RGB ↔ HSV (打包格式：H<<16 | S<<8 | V)
└─ COLOR_LERP_HSV                              → HSV 空间线性插值

颜色混合与 Alpha 处理
├─ MIX_COLOR                                   → 两色按权重混合
├─ CALC_ALPHA_COLOR                            → 带透明度的前景+背景融合
└─ SET_ALPHA_COLOR / RESET_ALPHA_COLOR         → 旧版兼容：设置/重置带 Alpha 颜色

调查发现函数库一共有6+2个进度条组件：
; ────────────────────────────────────────────────────────────────
字符制表式：
; ────────────────────────────────────────────────────────────────
1. @COLOR_BAR：最臃肿的实现。使用 FOR 循环逐个打印字符以PRINT和SETFONT系命令显示，内部集成了单独的 RGB 颜色渐变算法。只有经验进度条调用。
├─2. @PRINTLEVELBAR：COLOR_BAR 的包装函数，用于打印渐变效果的经验进度。
3. @BW_BAR：最纯粹的无颜色字符串输出，以两种字符代表填满（█）和空闲（▒），使用的是FOR循环的打印逻辑，一个个字符组装的。效率极低。
├─4.@Print_Bar：逻辑与@BW_BAR完全一致的渲染函数，永琳通自用。

5. @PRINT_COLORBAR：传统的双色/双字符表示的进度条渲染，调用 SETCOLOR 逐个字符打印。未谈及的所有进度条均由此渲染。
6. @HTML_COLORBAR：PRINT_COLORBAR的HTML实现，输出HTML格式的进度条字符串变量。需要HTML渲染的场景需要，目前只有开锁系统的进度条使用。
; ────────────────────────────────────────────────────────────────
图形式：
; ────────────────────────────────────────────────────────────────
7. @PRINT_RATE_BAR(EX)：图形条。使用 Emuera 原生的类shape渲染 PRINT_RECT 命令绘制图形，支持复杂的参数，精度和功能最为炸裂。

8. @LAYER_RECTBAR：为旧 Layer 系统准备的图形条，生成单色或双色的 <shape> 标签。最具现代化改造潜力。

现重构为3个组件，兼容所有旧函数封装接口：

字符式进度条（HTML <font> 实现，轻量、易混排）
├─ QOL_HTML_BARSTR                    → 核心生成器：组装HTML格式的字符串变量，支持 HSV 逐字符渐变、自定义字符
├─ PRINT_COLORBAR                     → 以HTML_PRINT直接渲染QOL_HTML_BARSTR()
├─ HTML_COLORBAR                      → 返回QOL_HTML_BARSTR（兼容旧接口）
├─ BW_BAR                             → 黑白/灰阶简洁版。返回QOL_HTML_BARSTR（兼容旧接口）
└─ COLOR_BAR                          → 带彩虹尾渐变的专用条（RGB 参数接口，已内部转QOL_HTML_BARSTR的 HSV实现）
像素级矩形进度条（<shape> 实现，高精度、现代感）
├─ HTML_RECT_BAR                      → 核心：像素级 HSV 渐变矩形条
├─ PRINT_RATE_BAR / PRINT_RATE_BAR_EX → 高精度分段条：支持双层、超限、间隙、对齐、粗细调节
└─ LAYER_RECTBAR                      → 重定向到 HTML_RECT_BAR（兼容旧接口）

; ────────────────────────────────────────────────────────────────
; 使用建议
; ────────────────────────────────────────────────────────────────
; • 所有渐变均使用 HSV 空间（COLOR_LERP_HSV），色彩过渡更鲜艳、自然，避免 RGB 直调的过暗/过曝
; • 字符条（QOL_HTML_BARSTR 系）适合文字混排、轻量 UI
; • 矩形条（HTML_RECT_BAR / PRINT_RATE_BAR_EX）适合血条、经验条、冷却条等需要平滑过渡的场合
; • 分段条（PRINT_RATE_BAR_EX）支持超限延伸、多层叠加、间隙、对齐，是最灵活的高级组件，允许高精度像素级拆分
; • 建议在主调用函数中开启 BITMAP_CACHE_ENABLE 1 以提升复杂 shape 渲染性能
