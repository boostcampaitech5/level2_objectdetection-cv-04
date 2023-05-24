# [level2-cv-04] Recycle Object Detection

- Project Period 2023/05/02 ~ 2023/05/18
- Project Wrap-Up Report [https://docs.google.com/document/d/186zCk5UyzSZIM15Qt9GxeNyVQkfd-4LiDaYM1MWZV8w/edit?usp=sharing](https://docs.google.com/document/d/186zCk5UyzSZIM15Qt9GxeNyVQkfd-4LiDaYM1MWZV8w/edit?usp=sharing)

## **✏️** Project Overview



![[Untitled](Recycle%20Object%20Detection%20Readme%20becffc1aba044f67916b08a876f30d02/Untitled.png)](https://file.notion.so/f/s/f9564bd6-c973-41dc-9c0a-c50f7f38d6b3/Untitled.png?id=e601154c-cd6a-48b7-b007-0d53ccb5e8bc&table=block&spaceId=da4b99d4-8977-4e20-b369-c7fbd6d0cf5d&expirationTimestamp=1684980415123&signature=RLa3mUxbkekOqzBeZmw0lUS6a3rLiMlMgs4Q_t2BHQ8&downloadName=Untitled.png)

분리수거는 자원의 순환을 촉진하는 방법입니다. 우리는 효율적으로 분리수거를 수행할 수 있도록 사진에서 쓰레기를 Detection 하는 모델을 만들어 이러한 문제점을 해결해보고자 합니다.🌎

- **Input :** 쓰레기 객체가 담긴 이미지가 모델의 input으로 사용됩니다. 이미지의 각 쓰레기 객체에 대한 bbox annotation은 COCO format으로 제공됩니다.
- **Output :** 모델은 bbox 좌표, 카테고리, score 값을 리턴합니다.
- **평가지표**: mAP50
- **프로젝트 주제**: 재활용 쓰레기 이미지를 10개 항목으로 분류 및 bbox 검출
    - 10 class : General trash, Paper, Paper pack, Metal, Glass, Plastic, Styrofoam, Plastic bag, Battery, Clothing
- **프로젝트 구현 내용, 컨셉, 교육 내용과의 관련성**
    - 10가지 범주를 기준으로 객체의 위치를 탐색 및 각 객체를 분류
- **활용 장비 및 재료(개발 환경, 협업 tool 등)**
    - 팀 구성: 5인 1팀
    - 컴퓨팅 환경: 인당 V100 GPU 서버를 VS code와 SSH로 연결하여 사용
    - 협업 툴: notion, git, slack, jira, live share, RabbitMQ
    - 실험관리: wandb

## 🙌 Members

| 강동화 | 박준서 | 서지희 | 장철호 | 한나영 |
| :---: | :---: | :---: | :---: | :---: |
| <img src = "https://user-images.githubusercontent.com/98503567/235584352-e7b0568f-3699-4b6e-869f-cc675631d74c.png" width="120" height="120"> | <img src = "https://user-images.githubusercontent.com/89245460/234033594-cb90a3c0-f0dc-4218-9e11-2abc8db2be67.png" width="120" height="120"> |<img src = "https://user-images.githubusercontent.com/76798969/234210787-18a54ddb-ae13-4554-960e-6bd45d7905fb.png" width="120" height="120">  | <img src = "https://avatars.githubusercontent.com/u/70846128?s=400&u=6309e4d3b06e87d1a400f130efb6d6b5d6198f7d&v=4" width="120" height="120" /> |<img src = "https://user-images.githubusercontent.com/76798969/233944944-7ff16045-a005-4e4e-bf59-632766194d7f.png" width="120" height="120" />|
| [@oktaylor](https://github.com/oktaylor) | [@Pjunn](https://github.com/Pjunn) | [@muyaaho](https://github.com/muyaaho) | [@JCH1410](https://github.com/JCH1410) | [@Bandi120424](https://github.com/Bandi120424) |



## **🌏** Contributions



| 팀원명 | 학습 모델 | 추가 작업 |
| --- | --- | --- |
| 강동화 | Cascade R-CNN, UniverseNet | EDA, 모델 리서치, neck 및 backbone network 리서치 |
| 박준서 | Cascade R-CNN | EDA, mmdetection 실험 세팅, RabbitMQ 사용한 GPU scheduler 구현, Augmentation 리서치 및 실험, 모델 앙상블 |
| 서지희 | DETR, FocalNet | GitHub setting, RabbitMQ 사용한 GPU scheduler 구현 |
| 장철호 | Cascade R-CNN | 모델 리서치, Augmentation 리서치 및 실험 |
| 한나영 | YOLOv5, v8 | EDA, Jira, 실험관리 spread sheet, notion template 구축, 
ultralytics 실험 세팅, Error Analysis, 모델 앙상블 |

![[Untitled](Recycle%20Object%20Detection%20Readme%20becffc1aba044f67916b08a876f30d02/Untitled%201.png)](https://file.notion.so/f/s/fdb7b464-8ae6-421a-b124-bf5e2b7474d4/Untitled.png?id=8d30a4ba-10fb-43d8-8b2b-5c2785588699&table=block&spaceId=da4b99d4-8977-4e20-b369-c7fbd6d0cf5d&expirationTimestamp=1684980719179&signature=Ye_Seh0ERItzWSWKtP3r0svZ6oRz6ZhqDb7_rq72gfU&downloadName=Untitled.png)

## **❓** Dataset & EDA


- 전체 이미지 개수 : 9754장 (학습 데이터: 4883장, 평가 데이터: 4871장)
- 10 class : General trash, Paper, Paper pack, Metal, Glass, Plastic, Styrofoam, Plastic bag, Battery, Clothing
- 이미지 크기 : (1024, 1024)
- 주요 문제점
    - 클래스별 박스의 분포에 불균형이 있었습니다. general trash, paper, plastic, plastic bag을 제외하고는 6% 미만의 분포를 보였습니다.
    - 대부분 10개 미만의 object를 포함하고 있었으나, 20개 이상의 object를 포함하는 이미지도 있었습니다. 이 경우에는 물체가 뭉쳐져 있거나, 가려져있는 경우도 많았습니다.
    - 빨대가 있는 커피 take-out 잔을 플라스틱과 종이로 구분하는 등 하나의 물체를 세세히 구분하는 경향을 확인할 수 있었습니다.
    - 일반쓰레기의 구분이 다소 모호하다고 생각했습니다.
    - 흐릿한 이미지가 존재하였습니다.
    - **모델 선정 및 분석**
        - **Cascade R-CNN:** 서로 다른 IOU threshold를 갖는 ROI head를 학습하여 COCO detection task에서 기존의 detector들 보다 좋은 성능을 보여주어 사용했습니다.
        - **YOLO v5 & v8**: 빠른 학습 속도 + 작은 사이즈의 객체 탐지
            
            YOLO는 single stage detector로 빠른 학습 속도가 장점입니다. 제한된 시간 내에 비교적 준수한 성능을 내고자 YOLO 모델을 선택하였습니다. 또한, 작은 사이즈 객체를 잘 탐지하는 것이 중요하다고 생각하여 **YOLOv5**와 **YOLOv8**으로 실험을 진행하였습니다.
            
        - **UniverseNet**: Coco benchmark 이외에 작은 bbox가 많은 benchmark를 생성하고, 이에 robust한 모델을 제작하였습니다. 실험에 사용한 모델은 **UniverseNet50-20.08d** 모델로, 여러 개의 서로 다른 조합으로 연결된 네트워크로 구성됩니다. 논문에서는 SyncBN을 사용했으나, 구현 상의 오류로 일반 BN을 사용했습니다.
        - **ATSS FocalNet:** Transformer를 CV에 적용한 DETR같은 모델이 있었지만 epoch을 100이상으로 해야 하는 등 성능이 별로 좋지 않았습니다. 이에 대해 Self Attention을 대체한 Focal Modulation Network를 사용한 **FocalNet**을 사용했습니다.

## **4. 프로젝트 수행 결과**



| Model | Cascade-RCNN
(swin-S) | Cascade-RCNN
(swin-B) | ATSS
(Focalnet) | UniverseNet | YOLOv5 |
| --- | --- | --- | --- | --- | --- |
| mAP 50 | 0.607 | 0.5697 | 0.55 | 0.584 | 0.5463 |


![[Image20230523172927.jpg](Recycle%20Object%20Detection%20Readme%20becffc1aba044f67916b08a876f30d02/Image20230523172927.jpg)](https://file.notion.so/f/s/099c6fca-4375-4f4f-9121-2a1e5cd7d139/Image20230523172927.jpg?id=c7caaead-63e3-4109-84d9-15f334a77e4c&table=block&spaceId=da4b99d4-8977-4e20-b369-c7fbd6d0cf5d&expirationTimestamp=1684980936858&signature=LjeKy7_yI20HkBfYw6G3ynriNrzox7dRkCv8oAMROyk&downloadName=Image20230523172927.jpg)
