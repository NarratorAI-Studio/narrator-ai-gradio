"""Static data — BGM, dubbing voices, narration styles, task type mappings."""

from __future__ import annotations

from typing import TypedDict


class BgmItem(TypedDict):
    name: str
    id: str


class DubbingItem(TypedDict):
    name: str
    id: str
    type: str
    tag: str


class NarrationStyle(TypedDict):
    genre: str
    name: str
    id: str


# --- Task type → API endpoint mapping ---
TASK_ENDPOINTS: dict[str, str] = {
    "popular-learning": "/v2/task/commentary/create_popular_learning",
    "generate-writing": "/v2/task/commentary/create_generate_writing",
    "fast-writing": "/v2/task/commentary/create_fast_generate_writing",
    "clip-data": "/v2/task/commentary/create_generate_clip_data",
    "fast-clip-data": "/v2/task/commentary/create_generate_fast_writing_clip_data",
    "video-composing": "/v2/task/commentary/create_video_composing",
    "magic-video": "/v2/task/commentary/create_magic_video",
    "voice-clone": "/v2/task/voice_clone/create",
    "tts": "/v2/task/text_to_speech/create",
}

# --- Narration style templates (pre-built learning_model_id) ---
NARRATION_STYLES: list[NarrationStyle] = [
    {"genre": "热血动作", "name": "热血动作-困兽之斗解说", "id": "narrator-20250916152104-DYsban"},
    {"genre": "热血动作", "name": "热血动作-战火祈愿解说", "id": "narrator-20251013135241-oscGNF"},
    {"genre": "热血动作", "name": "热血动作-亡命反杀解说", "id": "narrator-20251027094011-kvuJpH"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-栽赃陷害解说", "id": "narrator-20250916152053-nBcHXC"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-恶人成功解说", "id": "narrator-20250923153825-XjVolv"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-女性犯罪解说", "id": "narrator-20250929165427-wNiGuu"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-无间卧底解说", "id": "narrator-20250929180346-qZIrwc"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-金蝉脱壳解说", "id": "narrator-20250930115028-baMeEb"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-真相揭露解说", "id": "narrator-20250928113959-cceaBA"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-密室求生解说", "id": "narrator-20251024180040-xtbSzv"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-孤证追凶解说", "id": "narrator-20251027094241-FcEQRh"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-迟到正义解说", "id": "narrator-20251110134448-Wnbqcq"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-图灵测试解说", "id": "narrator-20251113154145-BHUwFE"},
    {"genre": "烧脑悬疑", "name": "烧脑悬疑-以恶制恶解说", "id": "narrator-20251202162015-vbNHYB"},
    {"genre": "励志成长", "name": "励志成长-师生情谊解说", "id": "narrator-20250918141539-NnpZlD"},
    {"genre": "励志成长", "name": "励志成长-职场逆袭解说", "id": "narrator-20250924181617-tdbfAK"},
    {"genre": "励志成长", "name": "励志成长-草根翻身解说", "id": "narrator-20250929165344-QhCZuq"},
    {"genre": "励志成长", "name": "励志成长-校园冒险解说", "id": "narrator-20250930115936-QUhgtx"},
    {"genre": "励志成长", "name": "励志成长-谎言揭露解说", "id": "narrator-20251027093930-ZjWryu"},
    {"genre": "爆笑喜剧", "name": "爆笑喜剧-乌龙伪装解说", "id": "narrator-20250918183013-ktylCA"},
    {"genre": "爆笑喜剧", "name": "爆笑喜剧-催泪反转解说", "id": "narrator-20250924170117-wDFCwI"},
    {"genre": "爆笑喜剧", "name": "爆笑喜剧-抗日整蛊解说", "id": "narrator-20250924170024-uzgpov"},
    {"genre": "爆笑喜剧", "name": "爆笑喜剧-人生互换解说", "id": "narrator-20250929171156-BrsDAQ"},
    {"genre": "爆笑喜剧", "name": "爆笑喜剧-欢喜冤家解说", "id": "narrator-20251020160131-vpQowB"},
    {"genre": "爆笑喜剧", "name": "爆笑喜剧-乌龙反转解说", "id": "narrator-20251015170653-OPraUg"},
    {"genre": "爆笑喜剧", "name": "爆笑喜剧-翁婿大战解说", "id": "narrator-20251208154841-PzYwtq"},
    {"genre": "灾难求生", "name": "灾难求生-绝境获救解说", "id": "narrator-20250919170450-ClVcgT"},
    {"genre": "灾难求生", "name": "灾难求生-绝境反杀解说", "id": "narrator-20250919170037-ARppif"},
    {"genre": "灾难求生", "name": "灾难求生-丧尸变异解说", "id": "narrator-20250929162226-vJHwms"},
    {"genre": "灾难求生", "name": "灾难求生-连锁困境解说", "id": "narrator-20250929163803-MSBmuw"},
    {"genre": "灾难求生", "name": "灾难求生-怪兽灭世解说", "id": "narrator-20250929181329-HkkCNd"},
    {"genre": "灾难求生", "name": "灾难求生-海洋求生解说", "id": "narrator-20251124153146-eTtang"},
    {"genre": "灾难求生", "name": "灾难求生-极限逃生解说", "id": "narrator-20251208135459-bQYqJl"},
    {"genre": "悬疑惊悚", "name": "悬疑惊悚-密室奇案解说", "id": "narrator-20250915161121-kwwIHs"},
    {"genre": "惊悚恐怖", "name": "惊悚恐怖-民俗鬼怪解说", "id": "narrator-20250922151737-YElQZc"},
    {"genre": "惊悚恐怖", "name": "惊悚恐怖-怨念起源解说", "id": "narrator-20250930113312-nEKWax"},
    {"genre": "惊悚恐怖", "name": "惊悚恐怖-无限轮回解说", "id": "narrator-20251124152521-BrEkBi"},
    {"genre": "惊悚恐怖", "name": "惊悚恐怖-新婚猎杀解说", "id": "narrator-20251124152748-jrljzu"},
    {"genre": "东方奇谈", "name": "东方奇谈-都市修仙解说", "id": "narrator-20250915154420-YVDLiW"},
    {"genre": "东方奇谈", "name": "东方奇谈-情蛊拉扯解说", "id": "narrator-20250919100408-vyXstO"},
    {"genre": "东方奇谈", "name": "东方奇谈-以善封神解说", "id": "narrator-20250929165601-LJlMZm"},
    {"genre": "东方奇谈", "name": "东方奇谈-志怪奇缘解说", "id": "narrator-20250929173453-PAPePO"},
    {"genre": "东方奇谈", "name": "东方奇谈-宫斗权谋解说", "id": "narrator-20251011164028-QdtnCh"},
    {"genre": "东方奇谈", "name": "东方奇谈-人狐情缘解说", "id": "narrator-20251020160213-vZhBdF"},
    {"genre": "家庭伦理", "name": "家庭伦理-偷听心声解说", "id": "narrator-20250915162937-zUrCtQ"},
    {"genre": "家庭伦理", "name": "家庭伦理-禁忌诱惑解说", "id": "narrator-20251013171543-hKWxyY"},
    {"genre": "情感人生", "name": "情感人生-亡命虐恋解说", "id": "narrator-20250926153249-iLajMr"},
    {"genre": "情感人生", "name": "情感人生-重返过去解说", "id": "narrator-20250929165350-MTiKrB"},
    {"genre": "情感人生", "name": "情感人生-宅斗权谋解说", "id": "narrator-20250929171320-lTlKVh"},
    {"genre": "情感人生", "name": "情感人生-亲情救赎解说", "id": "narrator-20250929173718-kXJmvj"},
    {"genre": "情感人生", "name": "情感人生-禁忌之恋解说", "id": "narrator-20250929180959-ErBYYg"},
    {"genre": "情感人生", "name": "情感人生-错过重逢解说", "id": "narrator-20250930113630-idjJQO"},
    {"genre": "情感人生", "name": "情感人生-隔代亲情解说", "id": "narrator-20250930114558-nbhPEa"},
    {"genre": "情感人生", "name": "情感人生-婚姻破裂解说", "id": "narrator-20250917165831-wGnJGP"},
    {"genre": "情感人生", "name": "情感人生-逆袭救场解说", "id": "narrator-20251016164408-DTSoSw"},
    {"genre": "情感人生", "name": "情感人生-宿命重逢解说", "id": "narrator-20251022114420-evOJCI"},
    {"genre": "情感人生", "name": "情感人生-赌局救赎解说", "id": "narrator-20251027094055-htirpB"},
    {"genre": "情感人生", "name": "情感人生-童年创伤解说", "id": "narrator-20251027094012-unpBYG"},
    {"genre": "情感人生", "name": "情感人生-初遇心动解说", "id": "narrator-20251027094054-KaFrWF"},
    {"genre": "情感人生", "name": "情感人生-宿敌相恋解说", "id": "narrator-20251030145038-mfCVGj"},
    {"genre": "情感人生", "name": "情感人生-为爱殉情解说", "id": "narrator-20251014165420-xPFhHA"},
    {"genre": "情感人生", "name": "情感人生-双向奔赴解说", "id": "narrator-20251106115918-wiEURB"},
    {"genre": "情感人生", "name": "情感人生-返乡救赎解说", "id": "narrator-20251113153731-DRupIR"},
    {"genre": "情感人生", "name": "情感人生-童话溯源解说", "id": "narrator-20251113154655-NnDifu"},
    {"genre": "情感人生", "name": "情感人生-绝命循环解说", "id": "narrator-20251124153657-ZBBwwL"},
    {"genre": "情感人生", "name": "情感人生-为爱搏命解说", "id": "narrator-20251124154511-hebvkH"},
    {"genre": "情感人生", "name": "情感人生-爱情复仇解说", "id": "narrator-20251009143826-RQIUFF"},
    {"genre": "情感人生", "name": "情感人生-商业联姻解说", "id": "narrator-20251009145048-CBygkT"},
    {"genre": "情感人生", "name": "情感人生-忘年之交解说", "id": "narrator-20251202160328-KhoIpc"},
    {"genre": "情感人生", "name": "情感人生-养老困境解说", "id": "narrator-20251202161600-Dvmdkf"},
    {"genre": "情感人生", "name": "情感人生-向阳而生解说", "id": "narrator-20251208134824-OYNnQX"},
    {"genre": "情感人生", "name": "情感人生-聋哑骗局解说", "id": "narrator-20251208135010-wLnfJr"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-欲望深渊解说", "id": "narrator-20250922174548-khkyvU"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-异族重生解说", "id": "narrator-20250929173012-AptTKd"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-魔咒救赎解说", "id": "narrator-20250929180156-XqhhcL"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-异能人觉醒解说", "id": "narrator-20250930120652-AsoYAz"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-超级英雄解说", "id": "narrator-20250930172223-dWNzYw"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-上帝视角解说", "id": "narrator-20251016164239-wfMPqn"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-替身悲歌解说", "id": "narrator-20251016164259-uZELkl"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-力量诅咒解说", "id": "narrator-20251027094046-bCETIG"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-天选之人解说", "id": "narrator-20251027094101-SjLFeA"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-跌落神坛解说", "id": "narrator-20251027094142-SRepnG"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-局中局解说", "id": "narrator-20251016160421-ULNnBv"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-时空信件解说", "id": "narrator-20251110134239-aPENMc"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-拯救末日解说", "id": "narrator-20251113154508-QbYCwS"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-魔法家族解说", "id": "narrator-20251113154927-ASgxrL"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-智商开挂解说", "id": "narrator-20251202161012-GXhovQ"},
    {"genre": "奇幻科幻", "name": "奇幻科幻-逆天改命解说", "id": "narrator-20251202160957-VKVxtY"},
    {"genre": "传奇人物", "name": "传奇人物-枭雄末路解说", "id": "narrator-20250929171126-ChYkGc"},
    {"genre": "传奇人物", "name": "传奇人物-人生抉择解说", "id": "narrator-20251124154053-aOUlJQ"},
]

STYLE_GENRES = sorted(set(s["genre"] for s in NARRATION_STYLES))

# --- BGM list ---
BGM_LIST: list[BgmItem] = [
    {"name": "说了再见-纯音乐", "id": "032d0c59-642e-4aca-8204-adae462ba5a3"},
    {"name": "KAMNH", "id": "379883b2-4717-4393-a83e-e3524f9f7415"},
    {"name": "Call of Silence", "id": "5527b36b-3f96-47ee-a819-ada7b2298907"},
    {"name": "Anacreon", "id": "0597d458-ae36-44b5-9906-2241af888754"},
    {"name": "Sold Out", "id": "e3c21731-e786-4fe7-8e23-72bcdb31d428"},
    {"name": "Time Back", "id": "d710d6ee-e261-4091-a8e0-6235912cd222"},
    {"name": "丧尽", "id": "addabcc5-e148-404a-80d5-ee062b7b1b96"},
    {
        "name": "River Flows in You",
        "id": "065b0fbb-16f3-4b5e-a326-e05279eb7fc3",
    },
    {"name": "城南花已开", "id": "57f28e03-5a17-4994-b283-1edd8ea5ff6a"},
    {"name": "Experience", "id": "a37bf537-2318-4bbe-acad-09cb7d44c816"},
    {
        "name": "梦里梦外都是你(纯音乐)",
        "id": "2786f115-c28c-472d-b8cd-0dec533aae4a",
    },
    {
        "name": "Morsmordre (莫斯莫多)",
        "id": "32fff769-b685-424f-b55f-47b1f8aa2795",
    },
    {"name": "青空", "id": "3cb141f6-8d5a-44f7-b46d-240d9557ff16"},
    {"name": "流动的地狱之河", "id": "0231782a-be51-446b-b83b-86e608650466"},
    {"name": "Sub Title", "id": "36b33b1d-1ade-4816-a940-babca92ee964"},
    {"name": "Conundrum", "id": "aebb2ff9-0e4d-4bb2-9619-51540225bc98"},
    {"name": "Free Loop", "id": "3b014674-df53-4101-907c-d1b0ecdbe9c8"},
    {"name": "我走后", "id": "394c9c8d-cae8-45ff-9eea-694ec3856d9a"},
    {
        "name": "Whisper of Hope",
        "id": "c67ec434-3196-411f-8628-2f5b77a30461",
    },
    {
        "name": "Bleeding Love",
        "id": "130f8a0d-0b7b-4b51-9055-da7398783acf",
    },
    {
        "name": "Italia e voi",
        "id": "2f9296d3-e73a-460b-8e2f-f4d11a63a3cd",
    },
    {"name": "Oriente", "id": "f780f960-cdab-4ee4-a052-ad4d5e329f89"},
    {
        "name": "The Grotto(Remix)",
        "id": "e562c0d1-5c26-4d27-b9b2-d02cd2296540",
    },
    {"name": "My Soul", "id": "50f81dda-edd1-4696-be99-4d4803cdbfab"},
    {"name": "幻昼", "id": "d84b6016-286c-4bc8-88fa-0e725c128354"},
    {"name": "You", "id": "ab6d968c-853a-4dfa-b252-b551808724b5"},
    {
        "name": "Doopravdy(Radio Edit)",
        "id": "593cae44-8f44-4e99-8486-338cf6e5dfee",
    },
    {"name": "Windy Hill", "id": "60f0a0a8-50de-4f23-a60f-8f2e4c2f9695"},
    {"name": "Tuesday(DJ版)", "id": "d92e6963-705a-4da4-9b1b-9d6a577f1822"},
    {"name": "Paris", "id": "20a796ae-e5a3-45d3-880e-2bf945d843d8"},
    {"name": "Lordly", "id": "f3aac6c0-2d46-4810-9eba-d63cea281959"},
    {
        "name": "Sacred Play Secret Place",
        "id": "71051df4-60ac-4719-96dc-b4669b4825af",
    },
    {
        "name": "Born A Stranger",
        "id": "601e9d9b-02a3-455b-8723-d088e10ae358",
    },
    {"name": "III", "id": "d6f2ded8-32cd-409a-a392-a9fb03e2f2fe"},
    {
        "name": "戒不掉(DJ cek7版)",
        "id": "651f1b42-9ef0-4a70-9b3b-20342a252e7e",
    },
    {
        "name": "Undead Funeral March",
        "id": "1ab19938-3734-4aab-ab21-3c420908bccd",
    },
    {"name": "New Face", "id": "34d40047-97de-4f18-972a-8a4b3f1bcb0f"},
    {"name": "Anak(DJ版)", "id": "08b69d40-538a-4ee7-99ed-2ef27182c00c"},
    {
        "name": "神经病之歌 (二胡)",
        "id": "1d57709d-ba16-4d54-b100-e731a04aa5bb",
    },
    {
        "name": "Not The One",
        "id": "b0f17b96-26c5-4010-b454-dd9fe7492a61",
    },
    {"name": "buttercup", "id": "067919a2-5f1b-4fba-8491-d8f662bdfb18"},
    {
        "name": "The Party Troll",
        "id": "f0480139-a8ff-4961-8a99-bc94307b4526",
    },
    {
        "name": "Mapleleaf Rag (SoloFull Length)",
        "id": "5dc2808f-568a-4b7c-9fc6-d76d6ae36edc",
    },
    {
        "name": "Comedy Detective",
        "id": "d610e2de-4726-48c1-8694-5db3c1e254ee",
    },
    {
        "name": "Darktown Strutters Ball",
        "id": "be612856-01b3-4173-bee6-26256a3b1490",
    },
    {"name": "Entire", "id": "61993870-bd4b-408f-a3d7-b566d7c39e32"},
    {
        "name": "Friction Looks",
        "id": "20610c89-ac07-4e54-8341-79fa0dca37f5",
    },
    {
        "name": "Happy Haunts",
        "id": "ca618841-a498-42da-aad6-ac511b8deff0",
    },
    {
        "name": "New Year's Anthem",
        "id": "08df1bf9-4b97-474c-a5a1-863cb085411a",
    },
    {
        "name": "Lovable Clown Sit Com",
        "id": "5e861d9a-7b50-4293-8243-1083d499c4f7",
    },
    {"name": "Rumba Sabor", "id": "3b969bf5-83ea-463d-9295-b45d8b81b7c6"},
    {"name": "Silver", "id": "e443e221-c610-49ff-a525-3e5dada1cf2d"},
    {"name": "Sunspots", "id": "eee8638e-bf28-47e5-b4b0-6f22f223dfbd"},
    {"name": "Very Right", "id": "be4a7797-1560-4145-9c12-876c9ae12e58"},
    {
        "name": "Lucid Dreamer",
        "id": "6aa98e8b-42d2-4574-8890-04b647c11fac",
    },
    {
        "name": "Take Me Down To The Fashion Show",
        "id": "5c1e223a-9dfd-4b55-a2ba-25a3920d6467",
    },
    {"name": "Nebula", "id": "77abbe7d-a535-4cc0-8bd3-dc1565c0f454"},
    {"name": "Jay Jay", "id": "5df44829-c56e-4a4f-9d6d-5c6e14c788d3"},
    {"name": "Retreat", "id": "af7116bd-2a6e-47c5-a96a-14a986dd7bb8"},
    {"name": "Snack Time", "id": "228b5866-9107-4842-af1d-441a5437b39d"},
    {"name": "Sugar Zone", "id": "1b6a8429-bf5a-40f1-8f13-a7df14697d55"},
    {
        "name": "Sunday Plans",
        "id": "32266b80-2a32-455e-a5cf-dd10238e50c6",
    },
    {
        "name": "Going, Going, Gone",
        "id": "b4a10425-25fb-499e-b8ff-177aacb74b11",
    },
    {
        "name": "If I Had a Chicken",
        "id": "5ea6400c-5a6f-438a-a6d5-74ab270a45c3",
    },
    {"name": "Payday", "id": "4dba749d-b8c1-4651-a0df-c9224f730e4b"},
    {
        "name": "Spring In My Step",
        "id": "d9b111ab-98f2-49e7-8c95-4f8986cab8a5",
    },
    {"name": "Water Lily", "id": "67da4ea1-c2de-4eb9-8158-db10cbb928e6"},
    {
        "name": "Whistling Down the Road",
        "id": "bccfdbf8-56b1-4517-8f28-ceca4888adc5",
    },
    {
        "name": "Otis McMusic",
        "id": "3c6e4522-3df2-40a7-883f-de8ca7a8bbd4",
    },
    {"name": "The Beacon", "id": "a8892805-4654-4a3e-bb94-9959f5b53ed2"},
    {
        "name": "Witch Parade Assassin",
        "id": "a4d529f1-44f1-473a-b6e2-99f70831dcc3",
    },
    {"name": "despair", "id": "a818dc74-a2d4-46e2-8404-8ed311b62e28"},
    {"name": "风居住的街道", "id": "de119e08-72a5-4931-ba0a-e154c9b0c012"},
    {
        "name": "夜、萤火虫和你",
        "id": "50a5c205-aeb1-453c-bcfd-d0edc3b215c5",
    },
    {"name": "所念皆星河", "id": "f51c22ca-bfc2-4585-9874-466765438846"},
    {"name": "Dogs of War", "id": "475388ec-3736-4fd7-bcff-9005fb803680"},
    {"name": "Epiphany", "id": "272cf79a-3167-4955-841f-13cceaa931cd"},
    {
        "name": "No Traces Left",
        "id": "2497727f-0a4d-4289-856f-b400671d688b",
    },
    {
        "name": "コープスパーテイー",
        "id": "7cd3faf1-8520-416b-8246-8b38a313cb6f",
    },
    {
        "name": "夜空的寂静 (钢琴曲)",
        "id": "0522f35d-5ced-4301-a537-29978f53bb95",
    },
    {
        "name": "瞬间的永恒 (钢琴曲)",
        "id": "f537aa7a-c0f0-4cf3-a828-aed553af2929",
    },
    {"name": "風の住む街", "id": "fc423aca-ae0c-406c-bf41-65af50d1a3a8"},
    {
        "name": "秋的思念 (钢琴曲)",
        "id": "aa571c23-130b-4d7d-b245-427d496d2563",
    },
    {"name": "MELANCHOLY", "id": "6bb3c9ac-6259-4bf1-aa06-d490d3bd1dd1"},
    {"name": "和煦的糖果风", "id": "2a37db49-e272-4450-b50d-56e1cb1b2108"},
    {
        "name": "Bloom of Youth (风华正茂)",
        "id": "19b11777-f136-414a-975f-d22f3437b9fc",
    },
    {"name": "Piano Ver", "id": "2a7ebf12-43df-487e-89ef-d0c50448396a"},
    {"name": "Dusk", "id": "82ef3493-23b7-49f9-b5e1-99e5c08c576e"},
    {
        "name": "The Truth That You Leave",
        "id": "4cf6536d-9d9e-426a-a45e-6423bef8a861",
    },
    {
        "name": "River flows in you",
        "id": "02f34ff5-9747-4f90-a9bd-00f7d6de0f8e",
    },
    {
        "name": "ベニスの爱(イタリア)",
        "id": "8704ec4e-0831-4397-a0bd-06be52d13906",
    },
    {"name": "寂静之空", "id": "a53268af-2bea-4113-848d-867f2e109ea2"},
    {"name": "穿越时空的思念", "id": "599354c1-e250-45fa-84cf-0c034481984b"},
    {
        "name": "十宗罪 (戏子多秋版)",
        "id": "bca122e6-1a0b-4ee4-b553-e5b6f3ef3280",
    },
    {
        "name": "The Truth That You Leave (钢琴曲)",
        "id": "895408f1-339f-4c36-87cd-d9f419d18227",
    },
    {
        "name": "Prelude_1 (JIEBOSS remix)",
        "id": "384f666b-4283-4760-8659-c4ffb9b9f2f9",
    },
    {
        "name": "Tuesday (Original Mix)",
        "id": "13b98aab-c6c0-4d26-99c5-b0b756f30346",
    },
    {
        "name": "The Grotto",
        "id": "ce26210c-83ea-4bde-b3b5-c5958ca9f56f",
    },
    {"name": "SCARSONG", "id": "37ff89af-15ae-46a0-872c-6425e575ae01"},
    {
        "name": "Crossing Winds (Original)",
        "id": "5bd025c7-2c5b-470d-b81d-45712ea3b047",
    },
    {
        "name": "Battle Without Honor or Humanity",
        "id": "a5ed2f3b-37d8-4dfd-b7b5-9003a4bfec12",
    },
    {"name": "Just Blue", "id": "b00f6b41-f878-4538-8429-874c82398985"},
    {"name": "Fader", "id": "287f103e-5ab4-4ddf-b34a-bb50a51597a2"},
    {
        "name": "Early Morning Dreams (Kled Mone Remix)",
        "id": "0887393a-8352-4ae3-a10e-bc7e29d45a1c",
    },
    {
        "name": "Astronomia 2K19 (Radio Edit)(1)",
        "id": "8eb1cc9e-6d45-409a-a9c5-433adc329428",
    },
    {
        "name": "Crazy Donkey",
        "id": "e3e3d3d8-922c-4e4f-8229-46cf431b7727",
    },
    {"name": "Megalobox", "id": "332f03d5-18cf-4a74-80f0-6fc13afd92eb"},
    {
        "name": "Twisted ( Original Mix)",
        "id": "4671eed0-58ad-4d8c-aac6-2a40efa32555",
    },
    {
        "name": "Into the Battlefield II",
        "id": "1ae12e8f-b2d9-4d09-9a9b-c014b0c2f783",
    },
    {"name": "单车", "id": "873a0764-96b5-4ae3-bdc6-fb296103c2c9"},
    {"name": "Cyberworld", "id": "acacdcb3-8314-406d-b475-927904796843"},
    {"name": "太阳照常升起", "id": "5754d763-51be-46c2-88fd-927395fdc2df"},
    {
        "name": "Hope Always",
        "id": "e0a1a79a-a9b1-43db-8c51-8864560ba771",
    },
    {"name": "送给未来的你", "id": "bee90c5d-9295-4c84-9d14-66c769efbbbb"},
    {"name": "Visions", "id": "478908e3-c615-4320-b303-4e17b1b087c8"},
    {
        "name": "Destiny & Honor",
        "id": "c8db6e06-c8d3-45ed-b61c-81c5c1b359fc",
    },
    {
        "name": "Approaching Nirvana - You",
        "id": "6048ab67-6a5a-4459-a443-2b1fc7b09ad4",
    },
    {"name": "Rise", "id": "9d405490-594b-431c-9547-69035bc3f83d"},
    {"name": "Go Time", "id": "5c55f219-1d1e-4485-84ee-9e9a10bfa569"},
    {
        "name": "He's a Pirate",
        "id": "e48f7a0a-6ad2-4bed-91f9-a78916bcc5d7",
    },
    {"name": "S.E.N.S", "id": "009c9658-a352-4e24-8d6a-3d82b1b850fb"},
    {
        "name": "Rags to Rings",
        "id": "8b46616e-46a8-4f86-acbb-ac3d396f0bfc",
    },
    {
        "name": "Adventure Time",
        "id": "7468d4ac-fd0a-4275-b456-ce60067d1641",
    },
    {
        "name": "Victory (Orchestral)",
        "id": "597a8509-ee9e-4187-b514-a73d3fa2f94e",
    },
    {
        "name": "Heart of Courage",
        "id": "b73a83db-23ab-4181-ac80-71a4ee7a2409",
    },
    {"name": "定风波", "id": "fcd6f48a-5a51-42fc-9d96-a6322ffd0f88"},
    {"name": "Lのテーマ", "id": "80a7d246-51d3-4af3-aebb-ebee442e9ae2"},
    {"name": "Beta-B", "id": "0b8650ef-52fe-45a6-9cfe-d0ef6608a039"},
    {
        "name": "The X-Files (Original Version)",
        "id": "04ca8401-0d54-4886-bcf7-e7f0ed354f36",
    },
    {
        "name": "Unresolved Issues",
        "id": "f5fa9c25-bec1-4f09-9fd3-9a1434bb912a",
    },
    {"name": "误入迷失森林", "id": "4d7e2f2d-a450-44a8-bffe-0d574e9e2604"},
    {
        "name": "写真の謎～銃を出す男たち)",
        "id": "49775167-46e9-413a-bf01-c2f4187c4216",
    },
    {
        "name": "推理 (オリジナルヴァーション)",
        "id": "094562d2-2564-406c-84cb-2f350ab60bc7",
    },
    {
        "name": "Old Threads",
        "id": "6d8c73ab-f5fa-4451-9f88-8ffae5d65d9c",
    },
    {"name": "I LOVE YOU", "id": "d1948082-ca2b-4c31-912d-b97df70bd72a"},
    {"name": "D1ofaquavibe", "id": "8c293f33-567d-4e76-81ee-743bfb9aab1f"},
    {"name": "幼女幻奏", "id": "774ab821-05b3-4644-84e9-2599922aac4e"},
    {"name": "小猫多鱼", "id": "c394025e-36b7-4b4e-bce8-ede845e69454"},
    {"name": "Frontier", "id": "262df46b-348d-45fa-8b05-80b87ffd1b66"},
    {
        "name": "馬鹿ふたり (两个笨蛋)",
        "id": "995ba0b9-d7a7-4522-b4fe-2de7b3664d33",
    },
    {
        "name": "你高兴就好 (Remix)",
        "id": "70d5b143-c1d1-42f4-bcca-dd708f442000",
    },
    {"name": "皇家萌卫", "id": "9b216955-2d76-4cb7-b59e-aff617c7c272"},
    {"name": "ProleteR", "id": "3de7a74d-a0e0-499b-8f7f-1fcd029eb5c4"},
    {
        "name": "我曾厌恶自己的本性 (快手版)",
        "id": "4e9a3cf2-4d08-4f37-aa50-ee68093f5f97",
    },
    {"name": "Title Theme", "id": "71d56c6e-e713-429d-93f7-15a6329c4b44"},
    {
        "name": "Betty Boop (Ghost Remix)",
        "id": "1ce78e11-7086-4af0-a7d3-ef1e4b3bc259",
    },
]

# --- Dubbing voices ---
DUBBING_LIST: list[DubbingItem] = [
    # 普通话 - 角色/影视
    {
        "name": "霸王别姬-程蝶衣",
        "id": "MiniMaxVoiceId02586",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "酱园弄-詹周氏",
        "id": "MiniMaxVoiceId10985",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "不说话的爱-木木",
        "id": "MiniMaxVoiceId13064",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "聊斋",
        "id": "MiniMaxVoiceId12982",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "蜡笔小新",
        "id": "MiniMaxVoiceId14640",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "我是余欢水-余欢水",
        "id": "MiniMaxVoiceId15111",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "唐伯虎点秋香-唐伯虎",
        "id": "MiniMaxVoiceId17399",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "人生大事-莫三妹",
        "id": "MiniMaxVoiceId17438",
        "type": "普通话",
        "tag": "角色",
    },
    {
        "name": "夏洛特烦恼-沈腾",
        "id": "MiniMaxVoiceId17643",
        "type": "普通话",
        "tag": "角色",
    },
    # 普通话 - 通用男声
    {
        "name": "浑厚旁白",
        "id": "MiniMaxVoiceId15619",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "知心哥哥",
        "id": "MiniMaxVoiceId15944",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "解说男声",
        "id": "MiniMaxVoiceId15553",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "温暖男声",
        "id": "MiniMaxVoiceId16317",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "乐天派男声",
        "id": "MiniMaxVoiceId15847",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "阳光男声",
        "id": "MiniMaxVoiceId15390",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "深邃旁白",
        "id": "MiniMaxVoiceId15257",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "利落男声",
        "id": "MiniMaxVoiceId15047",
        "type": "普通话",
        "tag": "通用男声",
    },
    {
        "name": "激昂旁白",
        "id": "MiniMaxVoiceId14983",
        "type": "普通话",
        "tag": "通用男声",
    },
    # 普通话 - 场景推荐
    {
        "name": "严肃大叔音-适合动作、冒险类",
        "id": "mercury_yunye_24k@serious",
        "type": "普通话",
        "tag": "动作冒险",
    },
    {
        "name": "严肃青年解说-适合动作、冒险类",
        "id": "mercury_yunxi_24k@serious",
        "type": "普通话",
        "tag": "动作冒险",
    },
    {
        "name": "气泡音男声-适合动作、冒险类",
        "id": "momoyuan_meet_24k",
        "type": "普通话",
        "tag": "动作冒险",
    },
    {
        "name": "慵懒调侃男声-适合动作、冒险类",
        "id": "jupiter_BV107DialogMale",
        "type": "普通话",
        "tag": "动作冒险",
    },
    {
        "name": "神秘女声-适合动作、冒险、恐怖、惊悚类",
        "id": "galaxy_fastv7_moyingxi@angry",
        "type": "普通话",
        "tag": "动作冒险",
    },
    {
        "name": "东北老妹儿-适合喜剧",
        "id": "mercury_ln-xiaobei_24k",
        "type": "普通话",
        "tag": "喜剧",
    },
    {
        "name": "幽默闲聊女声-适合喜剧",
        "id": "galaxy_fastv8_moxueqin",
        "type": "普通话",
        "tag": "喜剧",
    },
    {
        "name": "犀利青年音-适合喜剧",
        "id": "galaxy_fastv8_mowasi",
        "type": "普通话",
        "tag": "喜剧",
    },
    {
        "name": "恐惧感大叔音-适合恐怖、惊悚类",
        "id": "mercury_yunye_24k@fearful",
        "type": "普通话",
        "tag": "恐怖惊悚",
    },
    {
        "name": "恐惧低沉大叔音-适合恐怖、惊悚类",
        "id": "mercury_yunze_24k@fearful",
        "type": "普通话",
        "tag": "恐怖惊悚",
    },
    {
        "name": "不安男声-适合恐怖、惊悚类、科幻",
        "id": "mercury_yunxi_48k@embarrassed",
        "type": "普通话",
        "tag": "恐怖惊悚",
    },
    {
        "name": "松弛大叔音-适合爱情、剧情类",
        "id": "mercury_yunyang_24k@newscast",
        "type": "普通话",
        "tag": "爱情剧情",
    },
    {
        "name": "元气少女音-适合爱情、剧情类",
        "id": "mercury_xiaochen_48k",
        "type": "普通话",
        "tag": "爱情剧情",
    },
    {
        "name": "磁性御姐音-适合爱情、剧情类",
        "id": "yangjingv_meet_24k",
        "type": "普通话",
        "tag": "爱情剧情",
    },
    {
        "name": "燃爆男声解说-适合爱情、剧情类",
        "id": "mercury_yunxi_24k",
        "type": "普通话",
        "tag": "爱情剧情",
    },
    {
        "name": "快嘴直爽青年-适合科幻类",
        "id": "moxidu_meet_24k@kehuan",
        "type": "普通话",
        "tag": "科幻",
    },
    {
        "name": "磁性悬疑男声-适合科幻类",
        "id": "manchaozn_meet_24k@boya",
        "type": "普通话",
        "tag": "科幻",
    },
    {
        "name": "冷静青年解说-适合历史、战争类",
        "id": "mercury_yunxi_48k@calm",
        "type": "普通话",
        "tag": "历史战争",
    },
    {
        "name": "沉稳大叔音-适合历史、战争类",
        "id": "mercury_yunze_24k@documentary-narration",
        "type": "普通话",
        "tag": "历史战争",
    },
    {
        "name": "纪实磁性男声-适合历史、战争类",
        "id": "manchaozn_meet_24k@jilupian",
        "type": "普通话",
        "tag": "历史战争",
    },
    {
        "name": "沉稳御姐音-适合历史、战争类",
        "id": "liyuansong_meet_24k@tale",
        "type": "普通话",
        "tag": "历史战争",
    },
    # 英语
    {
        "name": "英语-腔调青年音",
        "id": "mercury_guy_48k",
        "type": "英语",
        "tag": "英语",
    },
    {
        "name": "英语-温柔御姐音",
        "id": "chilli_meet_24k",
        "type": "英语",
        "tag": "英语",
    },
    {
        "name": "英语-慵懒少年音",
        "id": "arielturner_meet_24k",
        "type": "英语",
        "tag": "英语",
    },
    {
        "name": "英语-儒雅大叔",
        "id": "mandygubler_meet_24k",
        "type": "英语",
        "tag": "英语",
    },
    # 日语
    {
        "name": "日语-元气少女音",
        "id": "galaxy_fastmultiv1_moyouli",
        "type": "日语",
        "tag": "日语",
    },
    {
        "name": "日语-中年男声",
        "id": "galaxy_fastmultiv1_mozhishu",
        "type": "日语",
        "tag": "日语",
    },
    {
        "name": "日语-沧桑大叔音",
        "id": "mercury_naoki_24k",
        "type": "日语",
        "tag": "日语",
    },
    # 韩语
    {
        "name": "韩语-儒雅男声",
        "id": "mercury_injoon_24k",
        "type": "韩语",
        "tag": "韩语",
    },
    {
        "name": "韩语-温柔御姐音",
        "id": "mercury_sunhi_48k",
        "type": "韩语",
        "tag": "韩语",
    },
    # 西班牙语
    {
        "name": "西班牙语-温柔女声",
        "id": "mercury_dalia_48k",
        "type": "西班牙语",
        "tag": "西班牙语",
    },
    {
        "name": "西班牙语-温柔大叔音",
        "id": "mercury_jorge_48k",
        "type": "西班牙语",
        "tag": "西班牙语",
    },
    {
        "name": "西班牙语-磁性大叔音",
        "id": "mercury_alvaro_24k",
        "type": "西班牙语",
        "tag": "西班牙语",
    },
    # 葡萄牙语
    {
        "name": "葡萄牙语-沉稳男声",
        "id": "mercury_donato_24k",
        "type": "葡萄牙语",
        "tag": "葡萄牙语",
    },
    {
        "name": "葡萄牙语-热情女声",
        "id": "mercury_francisca_48k",
        "type": "葡萄牙语",
        "tag": "葡萄牙语",
    },
    # 德语
    {
        "name": "德语-稳重大叔音",
        "id": "mercury_christoph_48k",
        "type": "德语",
        "tag": "德语",
    },
    {
        "name": "德语-气质御姐音",
        "id": "mercury_katja_48k",
        "type": "德语",
        "tag": "德语",
    },
    # 法语
    {
        "name": "法语-慵懒大叔音",
        "id": "mercury_alain_24k",
        "type": "法语",
        "tag": "法语",
    },
    {
        "name": "法语-优雅女神音",
        "id": "mercury_brigitte_24k",
        "type": "法语",
        "tag": "法语",
    },
    # 阿拉伯语
    {
        "name": "阿拉伯语-稳重御姐音",
        "id": "mercury_salma_48k",
        "type": "阿拉伯语",
        "tag": "阿拉伯语",
    },
    {
        "name": "阿拉伯语-慵懒男低音",
        "id": "mercury_hamdan_24k",
        "type": "阿拉伯语",
        "tag": "阿拉伯语",
    },
    # 泰语
    {
        "name": "泰语-撩耳解说男音",
        "id": "mercury_niwat_24k",
        "type": "泰语",
        "tag": "泰语",
    },
    {
        "name": "泰语-气质御姐音",
        "id": "mercury_premwadee_24k",
        "type": "泰语",
        "tag": "泰语",
    },
    # 印尼语
    {
        "name": "印尼语-青年男声",
        "id": "mercury_ardi_24k",
        "type": "印尼语",
        "tag": "印尼语",
    },
    {
        "name": "印尼语-温柔御姐音",
        "id": "mercury_gadis_48k",
        "type": "印尼语",
        "tag": "印尼语",
    },
]

DUBBING_LANGUAGES = sorted(set(d["type"] for d in DUBBING_LIST))
DUBBING_TAGS = sorted(set(d["tag"] for d in DUBBING_LIST))
