"""
Update course images in the local SQLite database to use production CDN URLs.
Run: python update_images.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "local.db")

# Mapping of course slug -> production CDN image URL
SLUG_TO_IMAGE = {
    "2020-winter-ap-us-history-free-response": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155afa8d69b9e4b7ee82e43_AP%20US%20History%20Free%20Response.jpg",
    "2020-winter-ap-world-history-free-response": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155afe47599001bdaf7cbfd_AP%20World%20History%20Free%20Response.jpg",
    "2020-summer-basic-english-learning-grades-1-2": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a696514fd68346eeeb68_Basic%20English%20Learning%20Grade1-2.jpg",
    "2021-summer-basic-geometry": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6175014a53242000bc7f4cc1_Basic%20Geometry.png",
    "2020-summer-basic-math-for-grade-2-3": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a77ad1e84b4ea2c524c6_Basic%20Math%20for%20Grade2-3.jpg",
    "2021-summer-inroduction-to-scratch-us-class": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bbe9726aac6903fe328f5_Introduction%20to%20Scratch%20(%20US%20).png",
    "2021-summer-inroduction-to-scratch-china-class": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bbe9726aac6903fe328f5_Introduction%20to%20Scratch%20(%20US%20).png",
    "cs202-introduction-to-scratch-g3-g5": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a85c63cf824574b50da2b8_intro%20to%20scratch.png",
    "cs304-introduction-to-java-g5-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6290fbd9ddf6bbb5793a7996_intro%20to%20java.png",
    "cs305-introduction-to-python-for-kenya-g4-g8": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a861eee8bcc8cd7c075e6b_intro%20to%20python.png",
    "cs306-introduction-to-web-development-for-kenya-g4-g8": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a867c89558fd178166c0fc_intro%20to%20web%20dev.png",
    "cs307-algorithm-with-java": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb94781adae704033c0baf_CS307%20-%20Algorithm%20with%20Java.png",
    "cs308-basics-of-web-development": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb95a3ba5b0b7c45061f57_CS308%20-%20Basics%20of%20Web%20Development.png",
    "cs401-introduction-to-java-for-kenya-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a86bc3a22a86887e3462ae_intro%20to%20Java.png",
    "2020-fall-close-reading-session-1-hamlet": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a1147e925115082ecf1d_Close%20Reading%20Session1%20Hamlet.jpg",
    "2020-winter-digital-art-workshop": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155b02b31fbafe20e219b13_Digital%20Art%20Workshop.jpg",
    "french-level-1-for-beginners-fr103": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/604eccfd1a63f07b2d575d28_French.jpg",
    "2021-winter-fr105-basic-french": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e139e22d857b53b1df2eb2_French.png",
    "fr105-french-class-for-beginners-g4-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e139e22d857b53b1df2eb2_French.png",
    "2020-fall-french": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a2dd5318f26f0f6bee1b_French.jpg",
    "2020-summer-geometry-g7-g10": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a91d87dc7de5b2171932_Geometry%20G7-G10%2B.jpg",
    "2021-spring-introduction-to-ancient-roman-ottoman-empire-hist102": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/617526ea28685f41555e0ecf_reading%20club%20g4-g6%20%E5%89%AF%E6%9C%AC.png",
    "2021-fall-hist305-european-history-g6-g12": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618fb0c04bdf486dfcf2b5e0_HIST305.jpg",
    "2021-winter-hist307-england-and-the-british-empire": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4933407d430540a39622_HIST307-test%20no%20tuition.png",
    "hist307-england-and-the-british-empire-g4-g6": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e13b6f3d3724977a2f0538_HIST307-England.png",
    "hist311-history-of-art": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb85896b4ad5fcc2e6bfb1_WRT408%20-%202023%20Summer.png",
    "hist312-history-of-japan": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb929a7189ac01d323e36d_HIST312%20-%20Japan.png",
    "2020-december-winter-history-camp-g5-g12-explore-ancient-egypt-greece": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155af2cf43d8f0fea6b4536_2020%20December%20Winter%20History%20Camp(%20G5%20-%20G12).jpg",
    "2021-summer-intro-to-web-development": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bd21be2252ba57efa7222_Intro%20%20to%20Web%20Development.jpg",
    "2020-summer-introduction-to-public-speaking": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155ac2d755a334f1300b791_IntroductionToPublicSpeaking.jpg",
    "2020-summer-introduction-to-geometry-g7-g10": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bcc28445d1c82ba9eee0e_cover1.png",
    "2020-winter-introduction-to-grade-3-math": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6175284d266d4a801a10bc20_Introduction%20to%20Grade%203%20Math.jpg",
    "2020-summer-introduction-to-grade-4-math": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155aaed6fae1b6e9739fed6_Introduction%20to%20Grade4%20Math.jpg",
    "2020-winter-introduction-to-grade-4-math": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155b21b56bc133d916dccc0_Introduction%20to%20Grade%204%20Math.jpg",
    "2021-summer-introduction-to-g4-math": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bcb9eb531b9f825a552c2_intro%20to%20grade%204%20math%20%E5%89%AF%E6%9C%AC.png",
    "2020-summer-introduction-to-grade-5-math": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6175298c41c3c880ce55367f_Introduction%20to%20Grade5%20Math.jpg",
    "2020-winter-introduction-to-grade-5-math": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6174fb0453242090227f387f_Introduction%20to%20Grade%205%20Math.jpg",
    "2020-summer-introduction-to-grade-6-math": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6174f726d02509db585a0310_Introduction%20to%20Grade%206%20Math.jpg",
    "2021-summer-introduction-to-python-games-dev": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/62a861eee8bcc8cd7c075e6b_intro%20to%20python.png",
    "2020-fall-introduction-to-python-china-class": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61752bdc192a7676a27afbcf_Introduction%20to%20Python.jpg",
    "2020-fall-introduction-to-python": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61752a85e70dd0505761386d_Introduction%20to%20Python.jpg",
    "2020-summer-introduction-to-web-development-with-python-javascript": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bd21be2252ba57efa7222_Intro%20%20to%20Web%20Development.jpg",
    "literature-analysis-la204": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/60b5db81999dc17eeace7d61_LA%20204.png",
    "literature-analysis-la205": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/614d9f54266cd61b08d0ee8c_LA205.jpg",
    "2021-fall-la206-literary-analysis-g3-g4": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618fab8297525729a51a26d2_LA206.jpg",
    "2021-winter-la207-literary-analysis-g3-g4": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4a47ae40a20845712e91_LA207%20%20%E8%80%81%E9%BC%A0%20no%20tuition.png",
    "la207-mrs-frizby-and-the-rats-of-nimh-g3-g4": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4a47ae40a20845712e91_LA207%20%20%E8%80%81%E9%BC%A0%20no%20tuition.png",
    "la208-diary-of-a-wimpy-kid-a-long-walk-to-water-g3-g4": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6290ec114f89143deca3ef50_LA208-%E5%A4%8F%E4%BB%A4%E6%97%B6-%E6%8E%A8%E8%BF%9F.png",
    "literature-analysis-la307": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/60b181f367986cef83cd55dc_LA%20307%20(1).png",
    "literature-analysis-la308": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/614e95e44145580725b31a4f_800657712247a1e7c2d52a1a80fa40c.jpg",
    "2021-fall-la309-literary-analysis-g4-g6": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd4cfee2aa7c1584547ac5_LA309%20%E6%8C%87%E7%8E%AF%E7%8E%8B%20no%20tuition.png",
    "la310-french-class-for-beginners-g4-g9-copy": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd47123ca60b2dd78b57d7_LA310%20%20%E6%95%B0%E6%98%9F%E6%98%9F%20no%20tuition.png",
    "la311-a-separate-peace-the-outsiders-g4-g6": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd41b8302a5e0d73fd7fef_LA311%20%E4%B8%80%E4%B8%AA%E4%BA%BA%E7%9A%84%E5%92%8C%E5%B9%B3%20no%20tuition.png",
    "literature-analysis-la405": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/60b5d8e7ca5d3a8ecb6eefb5_LA%20405%20(1).png",
    "literature-analysis-la406": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/614e9b7a84f75404062b5f7b_8f1ea80d9ee87307cd8cdd45d26de3d.jpg",
    "2021-fall-la408-literary-analysis-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618bd484510f0adb861806df_LA408.jpg",
    "la409-literary-analysis-g6": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd47c3e586a8a8fd4ff58b_LA409%20%E9%A3%98-%E5%B0%8F%E5%A6%87%E4%BA%BA%20no%20tuition.png",
    "la409-gone-with-the-wind-little-women-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61e13ce83d372488442f0938_LA409%20%E9%A3%98-%E5%B0%8F%E5%A6%87%E4%BA%BA.png",
    "la410-war-and-peace-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd423a5c5b0778ebbd0e11_LA410%20%E6%88%98%E4%BA%89%E4%B8%8E%E5%92%8C%E5%B9%B3%20no%20tuition.png",
    "la416-harry-potter-book-3-4-g3-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64b93312ee991bc33570e1af_LA416.png",
    "2020-fall-literacy-analysis-little-prince-and-treasure-island": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61752d18d1bd77e62278d0de_Reading%20Club%20A%20The%20Little%20Prince%20and%20Treasure%20Island.jpg",
    "2020-summer-literary-analysis-seminar-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155acf4a50e133b8a660105_Literary%20Analysis%20Seminar%20G6-G9.jpg",
    "2021-summer-pre-algebra-china-class": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bc74cb5292c2ca28372f1_poster.png",
    "2021-summer-introduction-to-algebra-ii": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/616bcf70ac007ba0fbef6444_post.png",
    "2020-summer-pre-algebra": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/61547bdcef9c358eec1a15ef_2020PreAlgebra.jpg",
    "2020-fall-reading-club-g3-g4": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a450da3fadd8cfdbd7d0_Reading%20Club%20G3%20-%20G4.jpg",
    "2020-fall-reading-club-g4-g6-2": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a5b5e5fb5e0cd6831278_Reading%20Club%20G4%20-%20G6%20third.jpg",
    "2020-fall-reading-club-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a62f3e69985861abe7d2_Reading%20Club%20G6%20-%20G9.jpg",
    "2020-fall-reading-club-g4-g6-1": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a548e5fb5e93238311a9_Reading%20Club%20G4%20-%20G6%20Another.jpg",
    "2020-summer-reading-club-g4-g5": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155ad52f4812ff5c914d65c_Reading%20Club%20G4-G5.jpg",
    "2020-summer-reading-club-g4-g6": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155ada59e31be960575bc30_Reading%20Club%20G4-G6.jpg",
    "sci403-introduction-to-fundamentalsin-science": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb938fbdc6d35c9c2515cb_sci-403.png",
    "spn102-spanish-class-for-beginners-g4-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/628efea46736c77670042f1b_SPN102.jpg",
    "spn103-spanish-class-for-beginners-iii-g4-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6290f82c9a6b934a26247b7d_SPN103.png",
    "2020-summer-us-history": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a8d78a70300ad0c66da2_ExploreHistory%20-%20US%20History.jpg",
    "2021-fall-creative-writing-wrt403": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/618d22d91c6a81d1bf0ef93c_WRT403.png",
    "wrt404-creative-writing-ii-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd49b57a651929a2f9ac62_WRT404%20%20no%20tuition.png",
    "wrt404-creative-writing-ii-g6-g9-10": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd49b57a651929a2f9ac62_WRT404%20%20no%20tuition.png",
    "wrt405-writing-workshop-china-class-g6-g9": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/63bd3c5304199df79620dd90_WRT405-China%20-%20no%20tuition.png",
    "wrt408-poem-writing": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/64bb85896b4ad5fcc2e6bfb1_WRT408%20-%202023%20Summer.png",
    "2020-summer-world-history": "https://cdn.prod.website-files.com/60306606d61c1d0f6d23ec21/6155a8236fae1bdc8839f09f_Explore%20History%20-%20World%20History.jpg",
}

def update():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    updated = 0
    missing = 0
    for slug, img_url in SLUG_TO_IMAGE.items():
        c.execute("UPDATE events SET img = ? WHERE slug = ?", (img_url, slug))
        if c.rowcount > 0:
            updated += 1
        else:
            missing += 1
            print(f"  WARNING: slug not found in DB: {slug}")

    conn.commit()
    conn.close()
    print(f"Updated {updated} course images, {missing} slugs not found in DB.")

if __name__ == "__main__":
    update()
