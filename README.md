# hmdbSpider
[toc]

---

## 0x01 简介

本程序用于爬取并比对QI和hmdb数据库中的数据，筛选需要的数据。

---

## 0x02 使用方法
* 爬取目标网站 `https://hmdb.ca/metabolites/HMDB0000792` 
* `HMDB0000792`是从QI中获取的数据ID
* 爬取数据后，比对QI和hmdb数据库中的数据，筛选`Blood` `Endogenous`的数据
* 比对结果保存在`data/result.csv`中

### 1. 安装依赖

```
pip install -r requirements.txt
```

### 2. 运行程序

```
python main.py
```
    
`

