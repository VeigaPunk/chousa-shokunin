# R57W1ExecStoreMap — lane capture store inventory (chousa r57 w1)

Seat `R57W1ExecStoreMap` (executor, leaf). Item: map `corpus/captures` — sorted listing with per-file sha256+size;
which of the 47 pinned keys have `.raw`/`.txt`; which keys are NOT pinned (identify each document from its bytes);
which files lack a raw/txt sibling; total bytes. Frozen claims read-only — no predicate/target/counter/control/recipe
touched. Lane write: this file only; no fleet-root or sibling-lane write; no network fetch; no git/jj mutation; no
tool installed (none needed). Snapshot `date -u` = **2026-10-27T08:53:36Z**, lane HEAD `e0e73e0` (the C2
after-receipt commit, landed after the dispatch tip `f9736a3`); the store is live (L1 fetch continues), so totals are
a timestamped snapshot — every size+sha was read twice 1.2 s apart with zero unstable files (`unstable: []`); by
08:58:30Z two more keys had landed (121 files / 62 keys).

## 1. Pinned set recomputed independently of the counter

`git ls-tree -r --name-only 6656f0770a1460d6ba73d9d2976f698a35311921 corpus/evidence` → every `*spans.tsv` with a
`capture_sha256` column → distinct `(id,url,capture_sha256)` triples = **47** (= frozen `SET_N`); key =
`sha256(url)[:24]`. Frozen counter re-run read-only at HEAD: `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5
UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0.

## 2. Inventory — 117 files, 60 keys, 58,051,237 bytes (08:53:36Z)

`PIN` = one of the 47 pinned triples; `EXT` = not pinned; `ABSENT` = no such file; `raw=<bytes>:<sha256>`.
```
001287c436f0e6b1d166ae8d PIN raw=352066:203b16907c2c953e49bb71310df2a5fd761d3f1798115ceb2ad6881cd01c17c5 txt=5599:67f6f2df8ce96d01673d8f2f740e663f55ed8324bbf804834562bf746740a1db
02aefcf570a7108e699d0990 PIN raw=6550066:efc216d4b2df006674aaeef579167aa6841ed27daf0ba78db2da8a30b66b00a7 txt=22631:32a5907e701fadee0138ba71899090c5b68848075ad34c9564d893c99c6dd616
09fc63de41f293d43d631c46 PIN raw=41404:2868753dcc8f039f2e648507b1ca0bebdd449b114741235e70a8f7e31508092e txt=12901:374d7dacf95c69cb58c6b85524c16eb638ee69c225effa4c207861821a762774
0ae65ac01b93119d3c2f3fed PIN raw=252991:c2aa0e12d45f33d01739952b858259fc97c14ab43be618cf865fcb5eededaf91 txt=27737:1e185358c52c3c8ba90970dd79a624df1e532841aa0a9ccb7be738236be9971d
0cebd3c84524295839ceaadd EXT raw=4321:1ab03b07ec7455b8fc104bbf3bd2ad37a4a6779908560cfc0125c10066a5005b txt=1:36a9e7f1c95b82ffb99743e0c5c4ce95d83c9a430aac59f84ef3cbfab6145068
0f33243fd7ac2fe88b85c1ba PIN raw=6209520:cb3ffbf5013e7a3a60e2c9408aef4fb65e2a23b58d785b57d8830a4c3d3c2a41 txt=190614:13a34aa9bb107eefeb8bed6a50a0d574af84ff77a66940e8b88ea895fea1182f
167e9db7dde3c998838e3469 PIN raw=52944:c9d610ad7a50f01b6d11488213698a8dd68b03e4e066135b96d7dbf5a31cd730 txt=15656:ba7b2aa64899861cd07bad79220c7d438b5c7664b96486c4b74618777a14dd31
16fe8487aa97b98576a0dbac PIN raw=415245:7b600fe3ee9bda2bd59f437a689451486f746af0c1daf2774aab2aec56b67e26 txt=61909:927ff71c6d499477c9cc7a3acf9ed7e335cd63b802850e5f39f5aa86a398d3a4
1c15b611118dee97e4105fcf PIN raw=460896:5d328bad901f488c4cff1dd073b55e30653b29c9c21c48700b926421cb84c9f7 txt=60153:c508913aba177ae4d33b29b7076f305bbac578a1ea11d39e30ddee2d787d563f
27d4865f201e99c1fed9f79b PIN raw=20698:f82a2b0208f5cd5514cb5454387c70a7666593882e2e561940c101eee400f8fb txt=3945:cd65aa9e26b41d8a0f7a260a7dfacf4cbf0b3fc59ab9dbef7bd7ab6ba1a98626
28750bcdf5d36cd90a7709fb PIN raw=6398584:0f426ea25661fbee4f2becd5bbf83b1c627d3eb1d0265a11d7c2f9d7504e8370 txt=63869:c799044be4e0e6e62ccf96175edc6f56490e5872569633eebf2a1606fdb694c6
32d1d24b24fce96d2a078ec0 PIN raw=12699:f1148b3678c2a5791a08c9ad3ac8d2c1b6627541da6fc9c5aee9070f80d0fc18 txt=2796:0288da6eab57c4284d44bef19694b0ab23ac0fbd47ab173f5ecd572a72cfeb7b
34fcefc159bf2ebbd1e09540 PIN raw=7787275:fe6eae45a1b0efb6bf0f9c5047cf2e0982410f985cb825d5e8c3cd6f393c67a1 txt=47473:065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b
3749141b52b2dbb2e0e821c3 PIN raw=231231:83a30baf0d47afce01c76ceabc84014f19af773b468566d828279d646a784597 txt=66770:0b3518bf2d2ba3047212d6f4ccb83dfd1cf01960e51acb324f7b74b6b2730573
3a8b45977cd111e45e3980a5 PIN raw=178056:16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763 txt=319599:471e558969d4ec3d7f795c4b499be79aa31c6fb1f16f3065563a3d0025ba85ea
412b146a2720ce6557268d05 PIN raw=447995:a045fa73c8f87f70b13b45c990631cab493014ad57e3133453e1e00242a14799 txt=144931:d37b64ed18a860f8e7795b8dcc1b808e788f0643e4936f9dbcaf6e61bbf3b101
4132ec1b265e60624523251f PIN raw=2171480:15673fb43980fa4bfbe3c98811f9a0b09995abb70be6a1b9e663d39ffcbc3ac0 txt=91084:2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997
42bac8830527d6f1bb125c49 PIN raw=20142:956b9ff47a701d45d190641fdd93c1bcdc71b5d52ebc063cdb41ebbf889226a1 txt=2969:4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671
44be8711b50a9daae2865b02 PIN raw=188708:6db150b47c9e157b4bbd7879f45501e450a87aebadcf03a064fda6205268b0f0 txt=53020:ab3427c377d1991032d5165cbb6f08bb6ea29d964dda78b2363811dc0c2b2ba4
453d492becd9a2f4632cb8dd PIN raw=276732:ba8dbc5a02a152733f822db2975ec2dc2d66639cf902a3913f7c47f60f23c42f txt=14064:6e2577b00e711bbbcc0170b6f598f08c39ce6cdc4ea2cb59cad5c4bc78e04186
4d89520fce540f1cf7cf9ef8 EXT raw=276945:44509f29779b4c6ffa6a145a72abdfcc866ad0939f847435319941b59ed0d58c txt=12621:5af2812b16353a96dcd69cbf01a96437f4761b3a66c28e4bbed2d7c9e842be4f
5233bf47babaa1ca2b49ed15 PIN raw=915236:7a0b198c663394cb3f5455553deb7d43df184992d8eb0db627410e1c98eae526 txt=118594:beac2b7feb425a8885927850ea79ed5e916339c6f5cd4b45c3abbf1753f49b05
53a92273a452a58f28368691 EXT raw=1203711:460121b411d754f94c597b8d20066c45901a729c5d88f7f86fb065057cb5da84 txt=ABSENT:-
5a631adb18988a1a2421ce75 PIN raw=17217:215843ee560afbcdcc6df00f6451cb62445c98bce7178821eb8da93f2a4ca723 txt=4146:e18eeb26a5a5902e10f0e0b25a9886d99bbbafcf8adfb85b7846bbd569d1ba92
62be15a474e866e4bef6c9d5 PIN raw=291615:b4ff9d41fde4432260d4adea247a86efe911a61dd1f63034b31dc8b229270be6 txt=61188:960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a
6dc68fd6b32ce9c8dfcebce8 PIN raw=129024:6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3 txt=157816:d4e7e5adc9f723d61852a6dffd559062ba3db5603c43ec158d96d6d4e564e112
6f545e6c16b6b568ea3f591b EXT raw=187186:c4bedad5079edccb8c33e453b19387b7809c42910d822cff2ab6c2dd8a97e5eb txt=21401:ceef80d97d95a143c297ff636234550f0b4aaaf07afed8252c94d117e8a9a7a0
6fe041acddaa1f4e6f6e9775 EXT raw=418774:d01795dd60264371ed4d81c77d4453446b333e8f9cbb322f7c7dfe9e1a9d8e7d txt=19242:71fed1a3bc95a7e1377ef86e364f0aa183f0885175c8f0dce459b818a861688f
712ec7bb981a9669a6921db7 EXT raw=18164:50e6ef118aaf66452bdbe37d5ebb3d665ebb9e33d51178d911fcd51d477b9357 txt=311:1443b149a9914773a70246b53ead3cbce172d6f5ad797b7cb8af974149e60bf6
7194acc65a18f6555e4b8893 PIN raw=713922:9315274a275172fe1cadacb8871264647211e50c07431e7fb127502554918d69 txt=36968:05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f
7800e2e1e2df3bc124b6b83e PIN raw=5676:9a2ed95a2657aa8e13b8378208beb22e95dfb169060ca186eab91e9b995e0b33 txt=5676:9a2ed95a2657aa8e13b8378208beb22e95dfb169060ca186eab91e9b995e0b33
7809d5114330a60527436b07 PIN raw=5066141:f701f59d953866710db8a8281dcb5f3e46d1cf34222c4602c3028ec477ad35a1 txt=30277:e9f66647ee5fb0fcb2e4879eede3ced218002d9126bd54868724b4a31e1ac000
78761b633aee2289e5874ce9 PIN raw=417054:2371dbefedce5587d8d31853e1c7d1e6390443900c9effaa643744d222f24102 txt=126093:35bdf1c1cbc337d4c93ce7c8f2ed51635894903ed1cf4c15d6d6acc9ecc7480c
9695437cac165bb4b6145deb EXT raw=16366:84df89a7fd74b5c13d892dc58ee3857ba9456f54d40f1d0720894be474855b2b txt=16366:84df89a7fd74b5c13d892dc58ee3857ba9456f54d40f1d0720894be474855b2b
a42feae4448612f949cc715f PIN raw=418774:d01795dd60264371ed4d81c77d4453446b333e8f9cbb322f7c7dfe9e1a9d8e7d txt=19242:71fed1a3bc95a7e1377ef86e364f0aa183f0885175c8f0dce459b818a861688f
a476f4128186c7976671ab54 EXT raw=71102:f8a124c08ad00ed6ff155d0fa4caef345c3383a88c2504d7406c09669a9103db txt=29974:8976b167b8f13d44566c5987e6d481279812f45b02c8aa07daeefabdf1e514b2
a9cf41709b6fa5028332d98c PIN raw=807648:7f97317417cc3796e483ec1b32e678c69399425e21ac5f0452506f3afea93f0c txt=83246:d24f2315aad72d7ba64faa65d2da70bd05702f7404ac63a624a0803ffe78b136
ad3010d2aee49a95e0c7cb0b EXT raw=4321:e96cdea38ef2646c7320f45a1e2d574cc5cdd283a4c4114f7bb9d7fd7ed81bf7 txt=1:36a9e7f1c95b82ffb99743e0c5c4ce95d83c9a430aac59f84ef3cbfab6145068
adf6ba934e813b2c326fa150 PIN raw=76273:f3cb44c44dd6b034dd0a126f16466f96e1dafe953e24bfd3b0aa09e2be2cdd5d txt=6650:ed4dde2ea950ba19f04b64593e9c8681b139baa21e8eb2f83fdbbb4f4bc1c748
b27ffd2f0161104c6a28c9f5 PIN raw=1455192:51550c5c6b0537f02162fa637c903f60044aef13f481c4e5c2111d7cd1bf1b57 txt=120386:23306b9f84c95b06008ab5e4a5deaeb9b0e937041f5239ec57792710480f1d5d
b502d4c6a6ee023bee6f8531 PIN raw=202174:b77d86ce5b6cdaa8df7db2226f339961fbfd5dcdf3896b926e19f93a5a9cfc51 txt=70165:e5b57b4875727b969a646b06b0df748e0efc8796aa1eeabc7c7ce5a2f2c85ac5
b539a80218080da56a75b624 PIN raw=801280:46d1866ce9afd51682e7e77cdf62612876da22c9bdbc9e8e299090128cb378f6 txt=1406840:ce30e73574e7b5c82c58d41a421d52bdb1c94ad7d57f0359e492e82f1b360046
b73f7e8dd5b0ace740e48046 PIN raw=29495:35c987c1446b0974e3f0edaa39de753201358843960004dd376b56c8046ffa27 txt=12775:603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b
b9ca2a4fdf9455867534f144 PIN raw=24185:2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1 txt=24185:2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1
bdff491a75c6abeda1d9c01d PIN raw=243929:ac0fad62ed9a11fa3bd135e78427329be30899df90946de7ac45e153974e6c44 txt=323728:55b4085c442fce1abf3ebef737344eb32fecf3e2b12fc781ad7a1e802eeac4e5
c71776bc3084de059b84569d EXT raw=477774:398968a032fe1e47e29f0369a3537de170ea3edc4716ecce5f13162ea5dc0365 txt=788869:ad6fd2cbad49a0b9ef306592b57f60328b493be76a7505b6efb6e9e14e253057
c7266931a1731db3ff6ae77d PIN raw=1140215:815bea41f8c249010fa11f1d374e5977db3bac5e50999ba190788bd4fc51fd07 txt=69789:03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd
c9d1e74c3ac8d9eb332c9770 PIN raw=372430:813ef2234d7616b40ac072f3f35558fc4ad46f051802aa2970d5cecc9616570c txt=211326:722d3ce9b16486e8f7246670c37511b959abe427dc31304234e3ab12e665d97c
cacddf3bbf780a4c7582bb17 PIN raw=88313:56c2f612d6b4d14d9575f92df6415f9879c4b726438a46a13ff9427a04d9ade6 txt=11676:3006510c0696d4664926428ab79cb7614db0fabd974602ac15962f5ba3a96466
ce16d57277fedfd4f0e7750e PIN raw=4771:8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5 txt=4771:8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5
cfa080b4046592eb9490a82c PIN raw=17592:95843e4ef72ec3ada97356022742dfebe6ff2ce82dd805b152d37f672e8ab614 txt=2661:892da7addf636f484580d4c9ea50f1199f2a39b5b8ec73ef7ad8b70a3260dfeb
d2a1cf3d2c385daee67c4afd EXT raw=22143:9c2529a4ef352908bd43bf4016c9307663993cc13bad118af36b953addc0b445 txt=5805:c3b95e83286eda1eb40ff1efc72025a0e9c11c561a6536014ca263c2399c6b62
d473754a0cbf8d3095255d5a EXT raw=1486070:47435e4b36ef7a9755663b77d57df90c5fc0dbba713e6cdce4238592b536da25 txt=ABSENT:-
d663d66e2d39f868d84b1781 PIN raw=14520:d03e7893d5241b9ae25c28a3d55cdfad73b3a8d57414dd9ac836302858a0edbd txt=3785:a5173d776e9349aa35531b8e2a217a8f1605d1c726e356e839722018b14fe3b2
d8b4f8f8829b813f16227893 EXT raw=1285794:1f84ddf0cb9da958658c81b0efdb79308144cdcc5fada97d842f9a7de86021c5 txt=ABSENT:-
de34c41f76e5a5c0e1f4d1a2 EXT raw=23522:1c59e61bf425882d45e890f5569eedb394d810d8eebf77b7d95e17e86c8de45e txt=12649:fbeb8e541a456b569133c228b7b84b355f4af0a83d06bcaf78744393af9e38cf
de9f5afc3809acbf61f4d5bb PIN raw=321559:f3181ed0af4178ce04fdca5e0570def229fb96d50fc92cd288fdbd1c6c3e50f3 txt=17547:7e3e3cf426a787a62b50fdae064e54ab28865a1ef5114cd0bf5687a87d2bd9d2
e84bfe97808591d23fe3266f PIN raw=343301:ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732 txt=10106:93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155
fd468a36d78ff156b6200946 PIN raw=1156890:72763389bbe95ab312de097125baa447370a244cb3f1b1bd3030b9956fb5abce txt=82903:90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc
fea98dc5a5a486c988dd415c PIN raw=178654:daa2c5d940fc20d0fab683e5e25b1f31a802d681d71319002449edf334029454 txt=95733:ead3a7dd4ba97ae0ef05620f314844badf6c3fef5428988e61e4e2a146772f60
TOTAL files=117 keys=60 bytes=58051237
```
`git ls-tree -rl HEAD corpus/captures/` → **97 files / 56,061,395 bytes** committed at `e0e73e0`; 20 files uncommitted
(`git status --porcelain corpus/captures` → 20 `??`), all EXT keys from this wave's C3 candidate fetches.
`du -sb corpus/captures` = 58,051,237 (file sum; dir inode adds 4096).

## 3. Pinned coverage (of the 47 recomputed triples)

- **46 of 47** pinned keys have a `.raw` **and** a `.txt`; for each the `.txt` is byte-identical to the campaign
  recipe on its `.raw` (re-verified here for all EXT captures too: `%PDF-` → `pdftotext -layout`; else UTF-8 decode;
  else `html_to_text` ⇒ identical sha256).
- The one pinned key with **neither** sibling: `e3ca8f4fdd15420b80096a75` = S105
  (`gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf`) — 3 `refetch.tsv` attempts, all `curl_rc=28`
  (timeout), no bytes; the wrap-up `.raw` was deliberately removed in `e0e73e0` ("record-less wrap-up S105 bytes
  removed") ⇒ C2's `UNREACHABLE=1` / `BYTE_BACKED=46`.
- Sibling audit over the whole store: **3 files lack a sibling** (the three orphan `.raw`, §4 — no `.txt`);
  **0 `.txt` files lack a `.raw`**.
- Item fragment "001287c436f0e6b1d166ae8d.txt exists without …" — verified: that key has **both** siblings (`.raw`
  352,066 B = the 科技查新检索服务平台 HTML page; `.txt` 5,599 B = its `html_to_text` recipe form, sha
  `67f6f2df8ce9…`), and the `.txt` sha **equals S104's pinned `capture_sha256`** while the `.raw` (`203b1690…`) does
  not — the pin is carried by the text form; `.txt == recipe(.raw)` holds.

## 4. The three orphans — identified from their own bytes

`pdftotext -layout <raw> -` on each (PDF 1.4 / 1.5 / 1.7). Source URLs recovered by matching `sha256(url)[:24]`
against candidate URLs from the lane's own citation text (`corpus/captures/b27ffd2f0161104c6a28c9f5.txt:1360-1377`
reference list) and the wave's scout reports; each match is exact (recomputed key == filename).

| key | what the bytes are | source URL (recomputed key == filename) | pinned? |
|---|---|---|---|
| `53a92273a452a58f28368691` | **国家卫生健康委员会公报 2021·07** (31 pp) — gazette reprinting *国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知 国卫办药政发〔2021〕16号*, and inside it 《药品临床综合评价管理指南（2021 年版 试行）》 | `https://www.nhc.gov.cn/bgt/201807sgf/202109/5e18d6d8d86e405bad64dd4a8b666310/files/1733795726978_35780.pdf` | no |
| `d473754a0cbf8d3095255d5a` | **抗肿瘤药品临床综合评价技术指南（2022 年版 试行）** (66 pp) — 国家药物和卫生技术综合评估中心 / 国家癌症中心 / 药具管理中心 | `https://www.hnysfww.com/data/article/1656481023744041713.pdf` | no |
| `d8b4f8f8829b813f16227893` | **儿童药品临床综合评价技术指南（2022 年版 试行）** (68 pp) — 国家儿童医学中心 | `https://www.hnysfww.com/data/article/1656481067585283603.pdf` | no |

These are the R2/R3 and R4/R6 documents the frozen C3 REFS table names, held as bytes but outside the C2 pinned set
(so correctly carrying no C2 verdict); at HEAD their only `refetch.tsv` rows are failures (`curl_rc=28` timeouts).

## 5. The other EXT keys (this wave's C3 candidate fetches; each attested by a successful `refetch.tsv` row)

`6f545e6c16b6b568ea3f591b` (S133, `tcmevidence.net/…6381676262587201848492833.pdf`) = 《药品临床综合评价管理指南
（2021 年版试行）》; `6fe041acddaa1f4e6f6e9775` (S133, `nhc.gov.cn/cms-search/downFiles/863665c…pdf`) = the 2020 cover
《药品临床综合评价管理指南（试行）》, byte-identical to S130's `a42feae4448612f949cc715f` (same raw sha `d01795dd…`)
under a second URL key — the "2021年版" trap the R3 scout documented; `a476f4128186c7976671ab54` (S132, catcm.org.cn
2021 notice page); `de34c41f76e5a5c0e1f4d1a2` (S131, gcpunion.org 〔2019〕80号 notice page); `4d89520fce540f1cf7cf9ef8`
(S131, qilu-pharma repost); `9695437cac165bb4b6145deb` (S134, 湖南药事服务网 release page); `d2a1cf3d2c385daee67c4afd`
(S137, phirda repost); `712ec7bb981a9669a6921db7` (S131, mp.weixin.qq.com — 311-byte text, bot wall);
`c71776bc3084de059b84569d` (S133, forten-sp.aliyuncs PDF); `0cebd3c84524295839ceaadd` / `ad3010d2aee49a95e0c7cb0b`
(takarabiomed PDFs, 1-byte text — image-only).

## 6. Findings for the L1's C3 build (reported, not patched)

1. **The three orphan `.txt` siblings exist in the git object store but not in the lane tree.** `git show
   6f3276b:corpus/captures/<key>.txt` (commit `6f3276b` = jj keep-ref side commit
   `refs/jj/keep/6f3276bc9ea52dfa711c6687efb0cfc3a25de34a`, **not** an ancestor of HEAD) yields blobs whose sha256
   equals my recomputed recipe of the committed `.raw` (`c040bc85…`, `7ea529e5…`, `520f663e…` — MATCH for all three).
   C3's `form_of()` reads `corpus/captures/<key>.txt` for a non-OLE/zip raw, so **a raw-only PDF yields no defined
   form and cannot bind** as the lane stands.
2. **Heading-rule check on those three blobs** (frozen rule, applied read-only): the gazette blob satisfies
   `药品临床综合评价管理指南` as a heading (line `药品临床综合评价管理指南`, empty prefix) with `2021年版` present ⇒
   R3-bindable material; the 抗肿瘤 blob's title is line-split (`抗肿瘤药品临床综合评价` / `技术指南`) and the 儿童 blob
   likewise ⇒ **the R4/R6 titles are not a heading** in their `pdftotext -layout` forms (token `2022年版` is present
   in both). Reported; no patch proposed.
3. **In-store material that already passes the frozen heading+token rule** (counter's `heading_title` semantics):
   `6f545e6c16b6b568ea3f591b` → R3 heading (line 3, empty prefix) + `2021年版` ✔; `a476f4128186c7976671ab54` →
   `附件：药品临床综合评价管理指南（ 2021 年版 试行）` (R3 heading + token) ✔ and `国家卫生健康委办公厅关于规范开展药品
   临床综合评价工作的通知` (R2 heading, prefix 10 chars) ✔; `de34c41f76e5a5c0e1f4d1a2` → `国家卫生健康委关于开展药品使用
   监测和临床综合评价工作的通知` (R1 heading, prefix 7) ✔. No R4/R5/R6 heading exists in any store capture.
4. `6fe041acddaa1f4e6f6e9775` and S130's `a42feae4448612f949cc715f` are **one document under two URL keys**
   (identical raw sha `d01795dd…` and identical `.txt`) — the key count over-counts distinct documents by one.

## 7. C2 state observed (frozen counter, read-only, at HEAD `e0e73e0`)

`python3 corpus/evidence/round57/c2-count.py` → `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1
BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0; DRIFTED = S083 S087 S113 S114 S121, all `absent=0`
(quotes still present) ⇒ no FRESHNESS-FLAG due. At dispatch the state was 43/47 with S100 S103 S105 S106 pending;
attempt-2/3 rows have since landed S100 S103 S106, and S105 is now UNREACHABLE (3 timed-out attempts ≥600 s apart).
Nothing in the frozen claim was modified.

## 8. Housekeeping

Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ExecStoreMap/` (TMPDIR + PYTHONDONTWRITEBYTECODE=1 set there; <50 MB,
nothing in /tmp) — **deleted before this report was filed**; only this report survives. Lane writes: this file only.
No git/jj mutation anywhere; frozen counters run read-only, never edited; no capture re-fetched (no network access).

VERDICT: the lane capture store was mapped (117 files / 60 keys / 58,051,237 B at 2026-10-27T08:53:36Z; 46 of 47
pinned keys carry both siblings, 3 files lack a sibling, and the three orphans are the 2021 gazette / 抗肿瘤 2022 /
儿童 2022 documents whose `.txt` forms live only in a non-ancestor side commit) — the map survived, and the
orphan-`.txt` / R4-R6-heading gaps that block C3 binding are reported, not patched.
