@echo off
chcp 65001 >nul
echo ==========================================
echo      EraTW Magic DLC 一键删除旧文件脚本
echo ==========================================
echo.
echo 本脚本将自动把旧文件移动到备份文件夹中
echo 请确保本脚本在游戏根目录或更新文件夹中运行
echo.
pause

set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "BACKUP_ROOT=backup_deleted_%TIMESTAMP%"

echo 创建备份文件夹: %BACKUP_ROOT%
if not exist "%BACKUP_ROOT%" mkdir "%BACKUP_ROOT%"

if exist "#双击LazyloadingV2.5开启游戏" (
    echo [删除] #双击LazyloadingV2.5开启游戏
    move "#双击LazyloadingV2.5开启游戏" "%BACKUP_ROOT%\#双击LazyloadingV2.5开启游戏" >nul
) else (
    echo [跳过] 文件不存在: #双击LazyloadingV2.5开启游戏
)
if exist "ERB\OBJ\CLASS\objname to id.txt" (
    echo [删除] ERB\OBJ\CLASS\objname to id.txt
    if not exist "%BACKUP_ROOT%\ERB\OBJ\CLASS" mkdir "%BACKUP_ROOT%\ERB\OBJ\CLASS" >nul
    move "ERB\OBJ\CLASS\objname to id.txt" "%BACKUP_ROOT%\ERB\OBJ\CLASS\objname to id.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\OBJ\CLASS\objname to id.txt
)
if exist "ERB\method_from_eratohoЯeverse\ぱにめーしょん\LAYER\旧LAYER.7z" (
    echo [删除] ERB\method_from_eratohoЯeverse\ぱにめーしょん\LAYER\旧LAYER.7z
    if not exist "%BACKUP_ROOT%\ERB\method_from_eratohoЯeverse\ぱにめーしょん\LAYER" mkdir "%BACKUP_ROOT%\ERB\method_from_eratohoЯeverse\ぱにめーしょん\LAYER" >nul
    move "ERB\method_from_eratohoЯeverse\ぱにめーしょん\LAYER\旧LAYER.7z" "%BACKUP_ROOT%\ERB\method_from_eratohoЯeverse\ぱにめーしょん\LAYER\旧LAYER.7z" >nul
) else (
    echo [跳过] 文件不存在: ERB\method_from_eratohoЯeverse\ぱにめーしょん\LAYER\旧LAYER.7z
)
if exist "ERB\method_from_eratohoЯeverse\ぱにめーしょん\ぱにめーしょん_Readme.txt" (
    echo [删除] ERB\method_from_eratohoЯeverse\ぱにめーしょん\ぱにめーしょん_Readme.txt
    if not exist "%BACKUP_ROOT%\ERB\method_from_eratohoЯeverse\ぱにめーしょん" mkdir "%BACKUP_ROOT%\ERB\method_from_eratohoЯeverse\ぱにめーしょん" >nul
    move "ERB\method_from_eratohoЯeverse\ぱにめーしょん\ぱにめーしょん_Readme.txt" "%BACKUP_ROOT%\ERB\method_from_eratohoЯeverse\ぱにめーしょん\ぱにめーしょん_Readme.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\method_from_eratohoЯeverse\ぱにめーしょん\ぱにめーしょん_Readme.txt
)
if exist "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\readme.txt" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\readme.txt
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗" >nul
    move "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\readme.txt" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\readme.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\readme.txt
)
if exist "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\私货.7z" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\私货.7z
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗" >nul
    move "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\私货.7z" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\私货.7z" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\私货.7z
)
if exist "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\详细更新日志.txt" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\详细更新日志.txt
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗" >nul
    move "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\详细更新日志.txt" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\详细更新日志.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\详细更新日志.txt
)
if exist "ERB\口上・メッセージ関連\個人口上\058 Meiling [美鈴]\新制美鈴口上Ver0.5C\新製美鈴口上ReadMe.txt" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\058 Meiling [美鈴]\新制美鈴口上Ver0.5C\新製美鈴口上ReadMe.txt
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\058 Meiling [美鈴]\新制美鈴口上Ver0.5C" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\058 Meiling [美鈴]\新制美鈴口上Ver0.5C" >nul
    move "ERB\口上・メッセージ関連\個人口上\058 Meiling [美鈴]\新制美鈴口上Ver0.5C\新製美鈴口上ReadMe.txt" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\058 Meiling [美鈴]\新制美鈴口上Ver0.5C\新製美鈴口上ReadMe.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\058 Meiling [美鈴]\新制美鈴口上Ver0.5C\新製美鈴口上ReadMe.txt
)
if exist "ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\readme.txt" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\readme.txt
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗" >nul
    move "ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\readme.txt" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\readme.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\readme.txt
)
if exist "ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\关于蝴蝶妖精的一些小事.txt" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\关于蝴蝶妖精的一些小事.txt
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗" >nul
    move "ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\关于蝴蝶妖精的一些小事.txt" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\关于蝴蝶妖精的一些小事.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\118 Larva [ラルバ]\拉尔瓦~永恒之蝶 - Moe茗\关于蝴蝶妖精的一些小事.txt
)
if exist "ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\M_KOJO_K140_絶頂 （詳細版）.7z" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\M_KOJO_K140_絶頂 （詳細版）.7z
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍" >nul
    move "ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\M_KOJO_K140_絶頂 （詳細版）.7z" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\M_KOJO_K140_絶頂 （詳細版）.7z" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\M_KOJO_K140_絶頂 （詳細版）.7z
)
if exist "ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\readme.txt" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\readme.txt
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍" >nul
    move "ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\readme.txt" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\readme.txt" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\140 Megumu [龍]\【140】龍\readme.txt
)
if exist "Emuera.NET 1824+v22+EMv18+EEv53 NAudio.exe" (
    echo [删除] Emuera.NET 1824+v22+EMv18+EEv53 NAudio.exe
    move "Emuera.NET 1824+v22+EMv18+EEv53 NAudio.exe" "%BACKUP_ROOT%\Emuera.NET 1824+v22+EMv18+EEv53 NAudio.exe" >nul
) else (
    echo [跳过] 文件不存在: Emuera.NET 1824+v22+EMv18+EEv53 NAudio.exe
)
if exist "Emuera_LazyLoadingV3.0_x64.exe" (
    echo [删除] Emuera_LazyLoadingV3.0_x64.exe
    move "Emuera_LazyLoadingV3.0_x64.exe" "%BACKUP_ROOT%\Emuera_LazyLoadingV3.0_x64.exe" >nul
) else (
    echo [跳过] 文件不存在: Emuera_LazyLoadingV3.0_x64.exe
)
if exist "resources\AI arts\87_別顔.webp" (
    echo [删除] resources\AI arts\87_別顔.webp
    if not exist "%BACKUP_ROOT%\resources\AI arts" mkdir "%BACKUP_ROOT%\resources\AI arts" >nul
    move "resources\AI arts\87_別顔.webp" "%BACKUP_ROOT%\resources\AI arts\87_別顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\AI arts\87_別顔.webp
)
if exist "resources\薮蛇绘\68_別立ち2_服_憤怒.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_服_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_服_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_服_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_服_憤怒.webp
)
if exist "resources\薮蛇绘\68_別立ち2_服_発情.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_服_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_服_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_服_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_服_発情.webp
)
if exist "resources\薮蛇绘\68_別立ち2_服_笑顔.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_服_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_服_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_服_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_服_笑顔.webp
)
if exist "resources\薮蛇绘\68_別立ち2_服_通常.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_服_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_服_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_服_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_服_通常.webp
)
if exist "resources\薮蛇绘\68_別立ち2_裸_憤怒.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_裸_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_裸_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_裸_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_裸_憤怒.webp
)
if exist "resources\薮蛇绘\68_別立ち2_裸_発情.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_裸_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_裸_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_裸_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_裸_発情.webp
)
if exist "resources\薮蛇绘\68_別立ち2_裸_笑顔.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_裸_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_裸_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_裸_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_裸_笑顔.webp
)
if exist "resources\薮蛇绘\68_別立ち2_裸_通常.webp" (
    echo [删除] resources\薮蛇绘\68_別立ち2_裸_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別立ち2_裸_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別立ち2_裸_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別立ち2_裸_通常.webp
)
if exist "resources\薮蛇绘\68_別顔2_吐息.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_吐息.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_吐息.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_吐息.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_吐息.webp
)
if exist "resources\薮蛇绘\68_別顔2_服_憤怒.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_服_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_服_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_服_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_服_憤怒.webp
)
if exist "resources\薮蛇绘\68_別顔2_服_発情.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_服_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_服_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_服_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_服_発情.webp
)
if exist "resources\薮蛇绘\68_別顔2_服_睡眠.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_服_睡眠.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_服_睡眠.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_服_睡眠.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_服_睡眠.webp
)
if exist "resources\薮蛇绘\68_別顔2_服_笑顔.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_服_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_服_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_服_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_服_笑顔.webp
)
if exist "resources\薮蛇绘\68_別顔2_服_通常.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_服_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_服_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_服_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_服_通常.webp
)
if exist "resources\薮蛇绘\68_別顔2_照れ.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_照れ.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_照れ.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_照れ.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_照れ.webp
)
if exist "resources\薮蛇绘\68_別顔2_裸_性交.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_裸_性交.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_裸_性交.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_裸_性交.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_裸_性交.webp
)
if exist "resources\薮蛇绘\68_別顔2_裸_愛撫.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_裸_愛撫.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_裸_愛撫.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_裸_愛撫.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_裸_愛撫.webp
)
if exist "resources\薮蛇绘\68_別顔2_裸_憤怒.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_裸_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_裸_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_裸_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_裸_憤怒.webp
)
if exist "resources\薮蛇绘\68_別顔2_裸_発情.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_裸_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_裸_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_裸_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_裸_発情.webp
)
if exist "resources\薮蛇绘\68_別顔2_裸_笑顔.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_裸_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_裸_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_裸_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_裸_笑顔.webp
)
if exist "resources\薮蛇绘\68_別顔2_裸_自慰.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_裸_自慰.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_裸_自慰.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_裸_自慰.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_裸_自慰.webp
)
if exist "resources\薮蛇绘\68_別顔2_裸_通常.webp" (
    echo [删除] resources\薮蛇绘\68_別顔2_裸_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\68_別顔2_裸_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\68_別顔2_裸_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\68_別顔2_裸_通常.webp
)
if exist "resources\薮蛇绘\9.別立ち_服_憤怒.webp" (
    echo [删除] resources\薮蛇绘\9.別立ち_服_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9.別立ち_服_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9.別立ち_服_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9.別立ち_服_憤怒.webp
)
if exist "resources\薮蛇绘\9.別立ち_服_笑顔.webp" (
    echo [删除] resources\薮蛇绘\9.別立ち_服_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9.別立ち_服_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9.別立ち_服_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9.別立ち_服_笑顔.webp
)
if exist "resources\薮蛇绘\9.別立ち_服_通常.webp" (
    echo [删除] resources\薮蛇绘\9.別立ち_服_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9.別立ち_服_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9.別立ち_服_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9.別立ち_服_通常.webp
)
if exist "resources\薮蛇绘\9.別顔_服_通常.webp" (
    echo [删除] resources\薮蛇绘\9.別顔_服_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9.別顔_服_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9.別顔_服_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9.別顔_服_通常.webp
)
if exist "resources\薮蛇绘\9_別立ち_服_憤怒.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_服_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_服_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_服_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_服_憤怒.webp
)
if exist "resources\薮蛇绘\9_別立ち_服_発情.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_服_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_服_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_服_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_服_発情.webp
)
if exist "resources\薮蛇绘\9_別立ち_服_笑顔.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_服_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_服_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_服_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_服_笑顔.webp
)
if exist "resources\薮蛇绘\9_別立ち_服_通常.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_服_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_服_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_服_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_服_通常.webp
)
if exist "resources\薮蛇绘\9_別立ち_裸_憤怒.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_裸_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_裸_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_裸_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_裸_憤怒.webp
)
if exist "resources\薮蛇绘\9_別立ち_裸_発情.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_裸_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_裸_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_裸_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_裸_発情.webp
)
if exist "resources\薮蛇绘\9_別立ち_裸_笑顔.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_裸_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_裸_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_裸_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_裸_笑顔.webp
)
if exist "resources\薮蛇绘\9_別立ち_裸_通常.webp" (
    echo [删除] resources\薮蛇绘\9_別立ち_裸_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別立ち_裸_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別立ち_裸_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別立ち_裸_通常.webp
)
if exist "resources\薮蛇绘\9_別顔_吐息.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_吐息.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_吐息.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_吐息.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_吐息.webp
)
if exist "resources\薮蛇绘\9_別顔_服_憤怒.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_服_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_服_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_服_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_服_憤怒.webp
)
if exist "resources\薮蛇绘\9_別顔_服_発情.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_服_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_服_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_服_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_服_発情.webp
)
if exist "resources\薮蛇绘\9_別顔_服_睡眠.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_服_睡眠.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_服_睡眠.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_服_睡眠.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_服_睡眠.webp
)
if exist "resources\薮蛇绘\9_別顔_服_笑顔.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_服_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_服_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_服_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_服_笑顔.webp
)
if exist "resources\薮蛇绘\9_別顔_服_通常.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_服_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_服_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_服_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_服_通常.webp
)
if exist "resources\薮蛇绘\9_別顔_汗.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_汗.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_汗.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_汗.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_汗.webp
)
if exist "resources\薮蛇绘\9_別顔_照れ.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_照れ.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_照れ.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_照れ.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_照れ.webp
)
if exist "resources\薮蛇绘\9_別顔_裸_性交.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_裸_性交.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_裸_性交.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_裸_性交.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_裸_性交.webp
)
if exist "resources\薮蛇绘\9_別顔_裸_愛撫.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_裸_愛撫.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_裸_愛撫.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_裸_愛撫.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_裸_愛撫.webp
)
if exist "resources\薮蛇绘\9_別顔_裸_憤怒.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_裸_憤怒.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_裸_憤怒.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_裸_憤怒.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_裸_憤怒.webp
)
if exist "resources\薮蛇绘\9_別顔_裸_発情.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_裸_発情.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_裸_発情.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_裸_発情.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_裸_発情.webp
)
if exist "resources\薮蛇绘\9_別顔_裸_笑顔.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_裸_笑顔.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_裸_笑顔.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_裸_笑顔.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_裸_笑顔.webp
)
if exist "resources\薮蛇绘\9_別顔_裸_自慰.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_裸_自慰.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_裸_自慰.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_裸_自慰.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_裸_自慰.webp
)
if exist "resources\薮蛇绘\9_別顔_裸_通常.webp" (
    echo [删除] resources\薮蛇绘\9_別顔_裸_通常.webp
    if not exist "%BACKUP_ROOT%\resources\薮蛇绘" mkdir "%BACKUP_ROOT%\resources\薮蛇绘" >nul
    move "resources\薮蛇绘\9_別顔_裸_通常.webp" "%BACKUP_ROOT%\resources\薮蛇绘\9_別顔_裸_通常.webp" >nul
) else (
    echo [跳过] 文件不存在: resources\薮蛇绘\9_別顔_裸_通常.webp
)
if exist "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\口上文件\.gitkeep" (
    echo [删除] ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\口上文件\.gitkeep
    if not exist "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\口上文件" mkdir "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\口上文件" >nul
    move "ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\口上文件\.gitkeep" "%BACKUP_ROOT%\ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\口上文件\.gitkeep" >nul
) else (
    echo [跳过] 文件不存在: ERB\口上・メッセージ関連\個人口上\012 Rumia [ルーミア]\露米娅~宵暗之花 - Moe茗\口上文件\.gitkeep
)
if exist "Generate_ERH.py" (
    echo [删除] Generate_ERH.py
    move "Generate_ERH.py" "%BACKUP_ROOT%\Generate_ERH.py" >nul
) else (
    echo [跳过] 文件不存在: Generate_ERH.py
)
if exist "erb_check.py" (
    echo [删除] erb_check.py
    move "erb_check.py" "%BACKUP_ROOT%\erb_check.py" >nul
) else (
    echo [跳过] 文件不存在: erb_check.py
)
if exist "免责声明.md" (
    echo [删除] 免责声明.md
    move "免责声明.md" "%BACKUP_ROOT%\免责声明.md" >nul
) else (
    echo [跳过] 文件不存在: 免责声明.md
)
if exist "Emuera_LazyLoadingV3.0_x86.exe" (
    echo [删除] Emuera_LazyLoadingV3.0_x86.exe
    move "Emuera_LazyLoadingV3.0_x86.exe" "%BACKUP_ROOT%\Emuera_LazyLoadingV3.0_x86.exe" >nul
) else (
    echo [跳过] 文件不存在: Emuera_LazyLoadingV3.0_x86.exe
)
if exist "SoundTouch.dll" (
    echo [删除] SoundTouch.dll
    move "SoundTouch.dll" "%BACKUP_ROOT%\SoundTouch.dll" >nul
) else (
    echo [跳过] 文件不存在: SoundTouch.dll
)
if exist "魔改版更新记录文档\指令集工具.xlsx" (
    echo [删除] 魔改版更新记录文档\指令集工具.xlsx
    if not exist "%BACKUP_ROOT%\魔改版更新记录文档" mkdir "%BACKUP_ROOT%\魔改版更新记录文档" >nul
    move "魔改版更新记录文档\指令集工具.xlsx" "%BACKUP_ROOT%\魔改版更新记录文档\指令集工具.xlsx" >nul
) else (
    echo [跳过] 文件不存在: 魔改版更新记录文档\指令集工具.xlsx
)
if exist "魔改版更新记录文档\画蛇又添足版自改emuera解释器相关说明.txt" (
    echo [删除] 魔改版更新记录文档\画蛇又添足版自改emuera解释器相关说明.txt
    if not exist "%BACKUP_ROOT%\魔改版更新记录文档" mkdir "%BACKUP_ROOT%\魔改版更新记录文档" >nul
    move "魔改版更新记录文档\画蛇又添足版自改emuera解释器相关说明.txt" "%BACKUP_ROOT%\魔改版更新记录文档\画蛇又添足版自改emuera解释器相关说明.txt" >nul
) else (
    echo [跳过] 文件不存在: 魔改版更新记录文档\画蛇又添足版自改emuera解释器相关说明.txt
)
if exist "魔改版更新记录文档\魔法版\EraTW 魔法DLC教程.docx" (
    echo [删除] 魔改版更新记录文档\魔法版\EraTW 魔法DLC教程.docx
    if not exist "%BACKUP_ROOT%\魔改版更新记录文档\魔法版" mkdir "%BACKUP_ROOT%\魔改版更新记录文档\魔法版" >nul
    move "魔改版更新记录文档\魔法版\EraTW 魔法DLC教程.docx" "%BACKUP_ROOT%\魔改版更新记录文档\魔法版\EraTW 魔法DLC教程.docx" >nul
) else (
    echo [跳过] 文件不存在: 魔改版更新记录文档\魔法版\EraTW 魔法DLC教程.docx
)
if exist "魔改版更新记录文档\魔法版\EraTW 魔法DLC料理介绍.xlsx" (
    echo [删除] 魔改版更新记录文档\魔法版\EraTW 魔法DLC料理介绍.xlsx
    if not exist "%BACKUP_ROOT%\魔改版更新记录文档\魔法版" mkdir "%BACKUP_ROOT%\魔改版更新记录文档\魔法版" >nul
    move "魔改版更新记录文档\魔法版\EraTW 魔法DLC料理介绍.xlsx" "%BACKUP_ROOT%\魔改版更新记录文档\魔法版\EraTW 魔法DLC料理介绍.xlsx" >nul
) else (
    echo [跳过] 文件不存在: 魔改版更新记录文档\魔法版\EraTW 魔法DLC料理介绍.xlsx
)

echo.
echo ==========================================
echo 操作完成！
echo 所有被删除的文件已移动到: %BACKUP_ROOT%
echo ==========================================
pause
