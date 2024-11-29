# 電影推薦系統
* 組員:曾德容、邱育霖

## 專案目的
* 建立個人化的媒體內容推薦系統

## 功能概述
* 本專題設計一個電影推薦系統，通過蒐集使用者觀看紀錄和偏好類型，運用 AI 模型以協同過濾演算法計算使用者可能喜好的電影類型，若院線片符合使用者喜好類型，將推薦給使用者。本系統提供以下功能：
    1. 猜喜歡推薦：基於相似使用者的喜好，推薦電影給目標使用者。
    2. 新片推薦：對應模型輸出的喜好類型，推薦符合條件的新上片。
    3. 互動功能：使用者可點擊推薦的電影海報，將其加入待播清單，方便日後觀看。

## 技術架構
### 2.1 系統架構
* 本系統分為 前端視窗交互 和 後端推薦邏輯：
    1. 前端視窗設計：
        ◦ 使用 Tkinter 製作使用者介面，包括「猜你喜歡」、「已觀看清單」和「待播清單」。 
        ◦ 提供圖形化互動功能，點擊電影海報可加入待播清單。 
    2. 後端推薦邏輯：
        ◦ 資料蒐集：從資料庫中提取每位使用者的觀看紀錄，包括觀看影片類型與時間。 
        ◦ 偏好計算：使用 AI 模型分析使用者喜好，計算與其他使用者的相似度。 
        ◦ 推薦清單過濾：將模型運算的相似使用者偏好，過濾新上檔的電影，符合使用者喜好者將呈現於推薦視窗。 
    3. 推薦模型：
        ◦ 使用協同過濾（Collaborative Filtering）算法： 
            ▪ 基於使用者的協同過濾：根據相似使用者的偏好進行推薦。 
            ▪ 結合新片過濾條件：篩選符合使用者偏好的新上片電影。 

### 2.2 流程設計
* 系統操作流程：
    1. 登入與驗證：
        ◦ 使用者輸入帳號與密碼。
            <p><img src="https://github.com/roberthsu2003/__2024_09_04_tvdi__/blob/main/%E5%AD%B8%E5%93%A1%E4%BD%9C%E6%A5%AD/%E9%9B%BB%E5%BD%B1%E6%8E%A8%E8%96%A6%E7%B3%BB%E7%B5%B1-De-Jung_Tseng/Project_Watch_Movie/Diagrams/Diagrams/1128_login_frame.png?raw=true" width=200></img></p>
        ◦ 系統對比使用者資料庫驗證後進入主視窗。 
            ![The main frame](https://github.com/roberthsu2003/__2024_09_04_tvdi__/blob/main/%E5%AD%B8%E5%93%A1%E4%BD%9C%E6%A5%AD/%E9%9B%BB%E5%BD%B1%E6%8E%A8%E8%96%A6%E7%B3%BB%E7%B5%B1-De-Jung_Tseng/Project_Watch_Movie/Diagrams/Diagrams/1128_main_frame.png?raw=true)

    2. 資料處理與推薦：
        ◦ 從資料庫中讀取該使用者的觀看紀錄，計算其偏好類型。 
        ◦ 通過模型匹配相似使用者的偏好。 
        ◦ 根據偏好推薦符合條件的新片，顯示於「猜你喜歡」區域。 
    3. 互動操作：
        ◦ 使用者可點擊「猜你喜歡」區域中的電影海報，將影片加入「待播清單」。 
            ![Click The Poster](https://github.com/roberthsu2003/__2024_09_04_tvdi__/blob/main/%E5%AD%B8%E5%93%A1%E4%BD%9C%E6%A5%AD/%E9%9B%BB%E5%BD%B1%E6%8E%A8%E8%96%A6%E7%B3%BB%E7%B5%B1-De-Jung_Tseng/Project_Watch_Movie/Diagrams/Diagrams/1128_main_frame_2.png?raw=true)
        ◦ 若點擊的電影已位於「待播清單」中，將跳出警示視窗。 
            ![Click The Poster Twice](https://github.com/roberthsu2003/__2024_09_04_tvdi__/blob/main/%E5%AD%B8%E5%93%A1%E4%BD%9C%E6%A5%AD/%E9%9B%BB%E5%BD%B1%E6%8E%A8%E8%96%A6%E7%B3%BB%E7%B5%B1-De-Jung_Tseng/Project_Watch_Movie/Diagrams/Diagrams/1128_main_frame_3.png?raw=true)

## 操作影片
    影片:11209python職能發展學院/專題_電影推薦系統_曾德容_邱育霖.mkv




