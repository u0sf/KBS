KB = {
    "startNodeId": "start",
    "nodes": {
        "start": {
            "id": "start",
            "category": "اختيار المشكلة",
            "title": "إيه المشكلة الأساسية اللي بتواجهك؟",
            "help": "اختار الأقرب للمشكلة. لو في أكتر من مشكلة، ابدأ بالأكثر تأثيرًا.",
            "type": "single",
            "options": [
                {"id": "slow", "label": "الجهاز بطيء/بيهنج", "desc": "فتح البرامج بطيء أو الجهاز تقيل", "next": "slow_1"},
                {"id": "no_internet", "label": "مفيش إنترنت", "desc": "Wi‑Fi متصل بس مفيش تصفح أو مفيش اتصال", "next": "net_1"},
                {"id": "overheat", "label": "سخونة/فصل مفاجئ", "desc": "حرارة عالية، مراوح شغالة بقوة، أو الجهاز يفصل", "next": "heat_1"},
                {"id": "battery", "label": "مشكلة بطارية/شحن", "desc": "البطارية بتخلص بسرعة أو الشاحن مش بيشحن", "next": "bat_1"},
                {"id": "boot", "label": "مش بيشتغل/مش بيقلع", "desc": "لازمات إقلاع، شاشة سوداء، أو لا يدخل ويندوز", "next": "boot_1"},
                {"id": "bsod", "label": "شاشة زرقاء/إعادة تشغيل", "desc": "Blue Screen أو Restart فجأة", "next": "bsod_1"},
                {"id": "storage", "label": "المساحة ممتلئة", "desc": "C ممتلئ، رسائل Low Disk Space", "next": "stor_1"},
                {"id": "keyboard", "label": "كيبورد/ماوس مش شغال", "desc": "زرار مش بتستجيب أو تقطيع", "next": "io_1"},
            ],
        },
        "slow_1": {
            "id": "slow_1",
            "category": "الجهاز بطيء",
            "title": "البطء حصل فجأة ولا تدريجي؟",
            "help": "المفاجئ غالبًا سببه تحديث/برنامج/فيروس أو امتلاء مساحة. التدريجي غالبًا تراكم برامج/حرارة/هارد.",
            "type": "single",
            "options": [
                {"id": "sudden", "label": "فجأة", "desc": "كان طبيعي وبقى بطيء مرة واحدة", "next": "slow_2a"},
                {"id": "gradual", "label": "تدريجي", "desc": "السرعة بتقل مع الوقت", "next": "slow_2b"},
            ],
        },
        "slow_2a": {
            "id": "slow_2a",
            "category": "الجهاز بطيء",
            "title": "فيه حاجة من دول حصلت قريب؟",
            "help": "اختار الأقرب.",
            "type": "single",
            "options": [
                {"id": "update", "label": "تحديثات/تعريفات", "desc": "Windows Update أو تعريف كرت شاشة/شبكة", "next": "slow_res_update"},
                {"id": "new_app", "label": "برنامج جديد", "desc": "ثبتت برنامج/أداة جديدة", "next": "slow_res_newapp"},
                {"id": "virus", "label": "أعراض فيروس", "desc": "إعلانات، استهلاك عالي، برامج بتفتح لوحدها", "next": "slow_res_malware"},
                {"id": "not_sure", "label": "مش متأكد", "desc": "مفيش حاجة واضحة", "next": "slow_3"},
            ],
        },
        "slow_2b": {
            "id": "slow_2b",
            "category": "الجهاز بطيء",
            "title": "الهارد عندك SSD ولا HDD؟",
            "help": "لو مش عارف: لو الجهاز قديم غالبًا HDD. SSD بيكون أسرع جدًا في الفتح.",
            "type": "single",
            "options": [
                {"id": "ssd", "label": "SSD", "desc": "فتح سريع عادةً", "next": "slow_3"},
                {"id": "hdd", "label": "HDD", "desc": "الهارد العادي (ميكانيكي)", "next": "slow_res_hdd"},
                {"id": "unknown", "label": "مش عارف", "desc": "مش متأكد", "next": "slow_3"},
            ],
        },
        "slow_3": {
            "id": "slow_3",
            "category": "الجهاز بطيء",
            "title": "وقت البطء، استخدام الرام/المعالج عالي جدًا؟",
            "help": "افتح Task Manager وشوف CPU و Memory لو دايمًا عالي.",
            "type": "single",
            "options": [
                {"id": "yes", "label": "أيوه عالي", "desc": "CPU أو Memory فوق 80% أغلب الوقت", "next": "slow_res_highusage"},
                {"id": "no", "label": "لا", "desc": "النِسب عادية", "next": "slow_res_general"},
            ],
        },
        "net_1": {
            "id": "net_1",
            "category": "مفيش إنترنت",
            "title": "المشكلة في جهاز واحد ولا كل الأجهزة على الراوتر؟",
            "help": "ده بيفرق هل المشكلة من الراوتر ولا من جهازك.",
            "type": "single",
            "options": [
                {"id": "one", "label": "جهاز واحد", "desc": "موبايل/لاب تاني شغالين", "next": "net_2_device"},
                {"id": "all", "label": "كل الأجهزة", "desc": "مفيش إنترنت لأي حد", "next": "net_res_router"},
            ],
        },
        "net_2_device": {
            "id": "net_2_device",
            "category": "مفيش إنترنت",
            "title": "الاتصال Wi‑Fi ظاهر Connected بس مفيش تصفح؟",
            "help": "ولا أصلًا مش عارف يتصل بالشبكة؟",
            "type": "single",
            "options": [
                {"id": "connected_no_web", "label": "Connected بس مفيش تصفح", "desc": "No Internet / Limited", "next": "net_res_dns"},
                {"id": "cant_connect", "label": "مش قادر يتصل بالـ Wi‑Fi", "desc": "بيطلب باسورد/يفشل", "next": "net_res_auth"},
                {"id": "ethernet", "label": "باستخدم كابل", "desc": "Ethernet فيه مشكلة", "next": "net_res_eth"},
            ],
        },
        "heat_1": {
            "id": "heat_1",
            "category": "سخونة/فصل مفاجئ",
            "title": "السخونة بتظهر أثناء لعب/برامج تقيلة؟",
            "help": "ولا حتى على الاستخدام الخفيف؟",
            "type": "single",
            "options": [
                {"id": "heavy", "label": "أثناء ضغط عالي", "desc": "Gaming/Rendering/Photoshop", "next": "heat_2"},
                {"id": "light", "label": "حتى استخدام خفيف", "desc": "تصفح/يوتيوب", "next": "heat_res_light"},
            ],
        },
        "heat_2": {
            "id": "heat_2",
            "category": "سخونة/فصل مفاجئ",
            "title": "المراوح صوتها عالي أو في اختناق تهوية؟",
            "help": "مثلاً لاب على مخدة، فتحات مسدودة، تراب.",
            "type": "single",
            "options": [
                {"id": "yes", "label": "أيوه", "desc": "صوت عالي/تهوية ضعيفة", "next": "heat_res_airflow"},
                {"id": "no", "label": "لا", "desc": "التهوية كويسة", "next": "heat_res_thermal"},
            ],
        },
        "bat_1": {
            "id": "bat_1",
            "category": "بطارية/شحن",
            "title": "المشكلة بطارية بتخلص بسرعة ولا مش بيشحن؟",
            "help": "اختار الأقرب.",
            "type": "single",
            "options": [
                {"id": "drain", "label": "بتخلص بسرعة", "desc": "الوقت قل بشكل واضح", "next": "bat_res_drain"},
                {"id": "nocharge", "label": "مش بيشحن", "desc": "النسبة ثابتة أو 0%/Plugged in", "next": "bat_2"},
            ],
        },
        "bat_2": {
            "id": "bat_2",
            "category": "بطارية/شحن",
            "title": "الشاحن/السوكت فيهم مشكلة واضحة؟",
            "help": "قطع/سخونة عند السوكت/لمبة الشاحن بتفصل.",
            "type": "single",
            "options": [
                {"id": "yes", "label": "أيوه", "desc": "فيه قطع/فصل", "next": "bat_res_charger"},
                {"id": "no", "label": "لا", "desc": "شكله سليم", "next": "bat_res_driver"},
            ],
        },
        "boot_1": {
            "id": "boot_1",
            "category": "مش بيقلع",
            "title": "فيه لمبات/صوت تشغيل ولا الجهاز ميت خالص؟",
            "help": "ده بيفرق بين مشكلة كهرباء ومشكلة إقلاع.",
            "type": "single",
            "options": [
                {"id": "dead", "label": "ميت خالص", "desc": "لا لمبة ولا مروحة", "next": "boot_res_power"},
                {"id": "on_no_boot", "label": "بيشتغل بس مش بيدخل", "desc": "شاشة سوداء/شعار/بيلف", "next": "boot_2"},
            ],
        },
        "boot_2": {
            "id": "boot_2",
            "category": "مش بيقلع",
            "title": "بيوصل لشعار ويندوز ثم يعيد التشغيل؟",
            "help": "ولا بيفضل Loading/Automatic Repair؟",
            "type": "single",
            "options": [
                {"id": "loop", "label": "Loop وإعادة تشغيل", "desc": "يعيد التشغيل في نفس النقطة", "next": "boot_res_loop"},
                {"id": "repair", "label": "Automatic Repair", "desc": "إصلاح تلقائي", "next": "boot_res_repair"},
                {"id": "black", "label": "شاشة سوداء بعد التشغيل", "desc": "مفيش صورة", "next": "boot_res_black"},
            ],
        },
        "bsod_1": {
            "id": "bsod_1",
            "category": "شاشة زرقاء/Restart",
            "title": "بتحصل بعد تعريف/تحديث جديد؟",
            "help": "زي تعريف كرت الشاشة/الواي فاي أو تحديث ويندوز.",
            "type": "single",
            "options": [
                {"id": "yes", "label": "أيوه", "desc": "بعد تحديث/تعريف", "next": "bsod_res_driver"},
                {"id": "no", "label": "لا", "desc": "بتحصل بدون سبب واضح", "next": "bsod_2"},
            ],
        },
        "bsod_2": {
            "id": "bsod_2",
            "category": "شاشة زرقاء/Restart",
            "title": "بتحصل أثناء ضغط عالي ولا حتى استخدام عادي؟",
            "help": "الضغط العالي ممكن يشير لحرارة/رام/باور.",
            "type": "single",
            "options": [
                {"id": "heavy", "label": "أثناء ضغط", "desc": "Gaming/Heavy apps", "next": "bsod_res_heatpower"},
                {"id": "normal", "label": "استخدام عادي", "desc": "تصفح/شغل بسيط", "next": "bsod_res_ramdisk"},
            ],
        },
        "stor_1": {
            "id": "stor_1",
            "category": "المساحة ممتلئة",
            "title": "المساحة الممتلئة على C (وويندوز)؟",
            "help": "لو C ممتلئ، الأداء والUpdates بيتأثروا.",
            "type": "single",
            "options": [
                {"id": "yes", "label": "أيوه C", "desc": "C شبه فاضي 0-5GB", "next": "stor_res_cfull"},
                {"id": "other", "label": "لا (قرص تاني)", "desc": "D/E إلخ", "next": "stor_res_other"},
            ],
        },
        "io_1": {
            "id": "io_1",
            "category": "كيبورد/ماوس",
            "title": "المشكلة في جهاز USB خارجي ولا كيبورد/تاتش باد اللاب؟",
            "help": "اختار الأقرب.",
            "type": "single",
            "options": [
                {"id": "usb", "label": "USB خارجي", "desc": "ماوس/كيبورد USB", "next": "io_res_usb"},
                {"id": "laptop", "label": "اللاب نفسه", "desc": "كيبورد اللاب أو التاتش باد", "next": "io_res_laptop"},
            ],
        },
    },
    "results": {
        "slow_res_update": {
            "title": "بطء بعد تحديث/تعريف",
            "severity": "warn",
            "summary": "غالبًا التعريف أو تحديث ويندوز سبب تحميل زائد أو تعارض. الأفضل ترجع خطوة للوراء وتثبت نسخة مستقرة.",
            "steps": [
                "افتح Settings → Windows Update → Update history وشوف آخر تحديثات.",
                "لو المشكلة بدأت بعد Update مباشرة: جرّب Uninstall latest update (لو متاح).",
                "لو تعريف كرت شاشة/واي فاي: افتح Device Manager → اسم الجهاز → Roll Back Driver (إن وُجد).",
                "اعمل Restart وشوف الأداء.",
                "لو البطء مستمر: شغّل فحص Malware (Windows Security) كاحتياط.",
            ],
            "extra": "لو انت على لاب، تأكد من وضع الطاقة Balanced/Best performance حسب الحاجة.",
        },
        "slow_res_newapp": {
            "title": "بطء بسبب برنامج جديد",
            "severity": "ok",
            "summary": "البرنامج الجديد ممكن يكون بيشتغل في الخلفية أو بيضيف Startup services.",
            "steps": [
                "افتح Task Manager → Startup apps واقفل أي برنامج مش ضروري.",
                "احذف البرنامج اللي اتثبت قريب (Settings → Apps).",
                "بعد الحذف اعمل Restart.",
                "لو محتاجه: نزّل نسخة أقدم/خفيفة أو بديل.",
            ],
            "extra": "أحيانًا أدوات الـ VPN/Antivirus الثقيلة بتسبب بطء واضح.",
        },
        "slow_res_malware": {
            "title": "اشتباه Malware/Adware",
            "severity": "warn",
            "summary": "الأعراض بتشير لبرامج ضارة أو إضافات متصفح. لازم تنظيف قبل أي حلول أخرى.",
            "steps": [
                "افصل الإنترنت مؤقتًا لو فيه Popup/إعلانات كثيرة.",
                "شغّل Windows Security → Full scan.",
                "من المتصفح: احذف Extensions الغريبة، وارجع الإعدادات الافتراضية إن لزم.",
                "راجع Programs installed وحذف أي برنامج مش معروف.",
                "لو استمر: شغّل Offline scan من Windows Security.",
            ],
            "extra": "تجنّب تنزيل برامج كراك أو أدوات تنظيف غير موثوقة.",
        },
        "slow_res_hdd": {
            "title": "هارد HDD (سبب شائع للبطء)",
            "severity": "ok",
            "summary": "لو نظامك على HDD، نقل النظام لـ SSD هو أكبر ترقية للأداء. مؤقتًا تقدر تقلل الحمل وتفريغ مساحة.",
            "steps": [
                "سيّب مساحة فاضية على C لا تقل عن 15–20GB.",
                "اقفل Startup apps غير الضرورية من Task Manager.",
                "فعّل Storage Sense (Settings → System → Storage).",
                "افتح Defragment and Optimize Drives وشغّل Optimize (لـ HDD فقط).",
                "لو تقدر: ركب SSD وانقل ويندوز عليه (Clone أو تثبيت جديد).",
            ],
            "extra": "لو الهارد بيطلع صوت غريب/أخطاء، اعمل Backup فورًا.",
        },
        "slow_res_highusage": {
            "title": "استهلاك CPU/Memory عالي",
            "severity": "ok",
            "summary": "فيه عملية/برنامج مسيطر على الموارد. تحديده من Task Manager هو أسرع طريق للحل.",
            "steps": [
                "افتح Task Manager → Processes ورتّب حسب CPU ثم Memory.",
                "لو Browser: اقفل Tabs الثقيلة وشوف Extensions.",
                "لو Antimalware Service: سيبه يخلص أو جدوله وقت فاضي.",
                "لو برنامج غير معروف: اعمل Scan واحذفه لو مش موثوق.",
                "لو الرام قليل (4GB/8GB): زيادة الرام بتفرق جدًا خصوصًا مع ويندوز 11.",
            ],
            "extra": "لو الاستخدام عالي طول الوقت حتى في Idle، غالبًا فيه خدمة/برنامج عالق أو Malware.",
        },
        "slow_res_general": {
            "title": "حلول عامة للبطء",
            "severity": "ok",
            "summary": "مجموعة خطوات آمنة بتحسن الأداء لمعظم الحالات بدون مخاطرة.",
            "steps": [
                "Restart للجهاز (مش Shutdown فقط).",
                "اقفل Startup apps غير الضرورية.",
                "تأكد أن C فيه مساحة فاضية كفاية.",
                "حدّث تعريفات أساسية (Chipset/Graphics) من موقع الشركة إن أمكن.",
                "شغّل Disk Cleanup و Storage Sense.",
            ],
            "extra": "لو المشكلة بتزيد مع السخونة، انتقل لقسم السخونة.",
        },
        "net_res_router": {
            "title": "المشكلة من الراوتر/الخط",
            "severity": "warn",
            "summary": "طالما كل الأجهزة متأثرة، ركّز على الراوتر أو مزود الخدمة.",
            "steps": [
                "افصل الراوتر من الكهرباء 30 ثانية ثم شغله.",
                "تأكد من كابل الـ DSL/الفايبر ثابت ولمبة الإنترنت ثابتة.",
                "جرّب كابل مختلف لو متاح.",
                "لو اللمبة بتفصل/تومض: اتواصل مع مزود الخدمة (ISP).",
            ],
            "extra": "لو الراوتر قديم أو حرارته عالية، حطه في مكان مهوي.",
        },
        "net_res_dns": {
            "title": "Connected لكن بدون إنترنت (DNS/Stack)",
            "severity": "ok",
            "summary": "غالبًا DNS أو إعدادات شبكة/كاش تسبب عدم تصفح رغم الاتصال.",
            "steps": [
                "Restart للراوتر والجهاز.",
                "من Settings → Network: اعمل Forget للشبكة ثم اتصل تاني.",
                "جرّب تغيير DNS لـ 1.1.1.1 و 8.8.8.8.",
                "افصل VPN لو شغال.",
                "جرّب شبكة تانية (Hotspot) لتأكيد المشكلة.",
            ],
            "extra": "لو Hotspot شغال والراوتر لا، يبقى المشكلة من الراوتر/الخط غالبًا.",
        },
        "net_res_auth": {
            "title": "مش قادر يتصل بالـ Wi‑Fi",
            "severity": "ok",
            "summary": "ممكن باسورد غلط/فلترة MAC/تعريف واي فاي أو إعداد أمان.",
            "steps": [
                "تأكد من الباسورد وإلغاء Caps Lock.",
                "Forget network ثم Reconnect.",
                "أعد تشغيل الراوتر.",
                "لو الشبكة 5GHz جرّب 2.4GHz (أقرب في التوافق).",
                "حدّث تعريف الـ Wi‑Fi من موقع الشركة إن أمكن.",
            ],
            "extra": "لو الأجهزة الأخرى بتتصل عادي، ركّز على تعريف الشبكة في جهازك.",
        },
        "net_res_eth": {
            "title": "مشكلة Ethernet",
            "severity": "ok",
            "summary": "غالبًا كابل/منفذ/تعريف. التشخيص يبدأ بتبديل الكابل والمنفذ.",
            "steps": [
                "بدّل الكابل وجرب منفذ مختلف في الراوتر.",
                "لو في لمبة على منفذ اللاب/الراوتر: هل بتنور؟",
                "Restart للجهاز.",
                "حدّث تعريف كرت الشبكة (Ethernet).",
            ],
            "extra": "لو مفيش لمبات نهائي: احتمال منفذ/كابل تالف.",
        },
        "heat_res_light": {
            "title": "سخونة حتى مع الاستخدام الخفيف",
            "severity": "warn",
            "summary": "ده غالبًا تراب/مراوح/معجون حراري أو برنامج شغال في الخلفية.",
            "steps": [
                "اقفل أي برنامج تقيل وتأكد من CPU في Idle.",
                "نضّف فتحات التهوية (هواء مضغوط بحذر).",
                "استخدم سطح صلب وارفع اللاب شوية لتحسين تدفق الهواء.",
                "لو الجهاز قديم: صيانة (تنظيف داخلي + تغيير معجون) عند فني موثوق.",
            ],
            "extra": "لو فيه ريحة حرق أو سخونة غير طبيعية جدًا: افصل فورًا.",
        },
        "heat_res_airflow": {
            "title": "اختناق تهوية/مراوح عالية",
            "severity": "ok",
            "summary": "تحسين التهوية والتنظيف بيحل نسبة كبيرة من مشاكل السخونة.",
            "steps": [
                "حط اللاب على سطح صلب، وتجنب المخدة/السرير.",
                "نضّف الفتحات بفرشة ناعمة أو هواء مضغوط.",
                "قلل إعدادات الجرافيكس/الفريمات في الألعاب.",
                "فعّل وضع Balanced أو خفّض Maximum processor state لو محتاج.",
            ],
            "extra": "Cooling pad يساعد لكن مش بديل للتنظيف.",
        },
        "heat_res_thermal": {
            "title": "سخونة تحت الضغط رغم تهوية جيدة",
            "severity": "warn",
            "summary": "ممكن معجون حراري قديم أو إعدادات طاقة/تعريفات.",
            "steps": [
                "حدّث تعريف كرت الشاشة.",
                "راقب الحرارة (لو متاح) — لو تعدي 95°C غالبًا فيه مشكلة تبريد.",
                "نظّف المراوح داخليًا لو تقدر بأمان أو عند فني.",
                "تغيير المعجون الحراري غالبًا يحل المشكلة في الأجهزة القديمة.",
            ],
            "extra": "لو الجهاز يفصل (thermal shutdown) لازم معالجة تبريد بسرعة.",
        },
        "bat_res_drain": {
            "title": "البطارية بتخلص بسرعة",
            "severity": "ok",
            "summary": "غالبًا إعدادات طاقة/سطوع/برامج خلفية أو تدهور البطارية مع العمر.",
            "steps": [
                "قلل سطوع الشاشة وفعّل Battery saver.",
                "اقفل Apps في الخلفية (Settings → Apps → Startup/Background).",
                "تأكد مفيش برنامج بيستهلك GPU/CPU باستمرار.",
                "لو البطارية قديمة: راجع Battery report (Windows) لتقييم السعة.",
            ],
            "extra": "الألعاب والفيديو 4K بيستهلكوا البطارية بسرعة طبيعي.",
        },
        "bat_res_charger": {
            "title": "مشكلة شاحن/سوكت",
            "severity": "warn",
            "summary": "لو فيه فصل/قطع، احتمال الشاحن أو منفذ الشحن محتاج تغيير/صيانة.",
            "steps": [
                "جرّب شاحن أصلي آخر (نفس الفولت/الأمبير) لو متاح.",
                "تأكد من نظافة منفذ الشحن وعدم وجود لعب/ارتخاء.",
                "جرّب شحن من منفذ مختلف لو USB‑C (إن كان يدعم).",
                "لو السوكِت بيفصل باللمس: صيانة عند فني.",
            ],
            "extra": "تجنب استخدام شواحن غير أصلية بقدرة غير مناسبة.",
        },
        "bat_res_driver": {
            "title": "مش بيشحن رغم أن الشاحن سليم",
            "severity": "ok",
            "summary": "أحيانًا يكون تعريفات البطارية/إدارة الطاقة سبب المشكلة.",
            "steps": [
                "Restart للجهاز.",
                "افصل الشاحن وأعد توصيله بعد دقيقة.",
                "من Device Manager: Battery devices → Disable/Enable (بحذر) أو Update driver.",
                "حدّث BIOS/firmware من موقع الشركة لو فيه تحديثات طاقة.",
            ],
            "extra": "لو البطارية 0% دائمًا حتى مع الشحن: احتمال بطارية تالفة.",
        },
        "boot_res_power": {
            "title": "الجهاز ميت خالص (Power)",
            "severity": "warn",
            "summary": "مشكلة كهرباء/شاحن/بطارية/زر تشغيل. اتعامل بحذر.",
            "steps": [
                "جرّب مقبس كهرباء مختلف.",
                "لو لاب: جرّب تشغيل بالشاحن فقط (بعد فصل البطارية لو قابلة للفصل).",
                "اعمل Power reset: افصل الشاحن واضغط زر التشغيل 15 ثانية.",
                "لو مفيش استجابة: غالبًا محتاج فني (شاحن/بوردة).",
            ],
            "extra": "لو فيه ريحة حرق أو سخونة في الشاحن: افصل فورًا.",
        },
        "boot_res_loop": {
            "title": "Boot loop (إعادة تشغيل)",
            "severity": "warn",
            "summary": "ممكن ملفات نظام تالفة أو تعريف/تحديث أو مشكلة هارد/رام.",
            "steps": [
                "افصل أي USB خارجي (فلاشة/هارد).",
                "ادخل Advanced startup (لو متاح) وجرب Safe Mode.",
                "لو دخل Safe Mode: احذف آخر تعريف/برنامج اتثبت.",
                "شغّل Startup Repair أو System Restore لو متاح.",
            ],
            "extra": "لو بتتكرر مع أصوات هارد/بطء شديد: اعمل Backup فورًا لو قدرت.",
        },
        "boot_res_repair": {
            "title": "Automatic Repair",
            "severity": "warn",
            "summary": "النظام بيحاول يصلح الإقلاع. غالبًا حلها بإصلاح ملفات أو استعادة نقطة.",
            "steps": [
                "اختار Advanced options → Troubleshoot.",
                "جرّب System Restore لو فيه نقطة.",
                "جرّب Startup Repair.",
                "لو فشل: فكّر في Reset this PC (Keep my files) كحل أخير.",
            ],
            "extra": "قبل أي Reset، لو تقدر خد Backup للملفات المهمة.",
        },
        "boot_res_black": {
            "title": "شاشة سوداء بعد التشغيل",
            "severity": "warn",
            "summary": "ممكن مشكلة شاشة/تعريف كرت شاشة/كابل/وضع عرض.",
            "steps": [
                "جرّب زيادة السطوع والتأكد من الشاشة شغالة.",
                "لو Desktop: تأكد من كابل HDMI/DP وتبديله.",
                "جرّب توصيل شاشة خارجية (للاب) لتحديد هل المشكلة من الشاشة الداخلية.",
                "لو بتسمع صوت ويندوز بس بدون صورة: احتمال تعريف/Display.",
            ],
            "extra": "لو لا صورة ولا صوت: ارجع لسيناريو الإقلاع/الطاقة.",
        },
        "bsod_res_driver": {
            "title": "شاشة زرقاء بسبب تعريف/تحديث",
            "severity": "warn",
            "summary": "أفضل حل سريع هو الرجوع لتعريف مستقر أو إزالة التحديث المسبب.",
            "steps": [
                "ادخل Safe Mode لو بتتكرر بسرعة.",
                "Roll back driver أو احذف التعريف ثم ثبّت نسخة مستقرة من موقع الشركة.",
                "احذف آخر تحديث ويندوز لو بدأ بعده مباشرة.",
                "شغّل Windows Memory Diagnostic كتحقق إضافي.",
            ],
            "extra": "لو عندك كود خطأ في الشاشة الزرقاء، ممكن يحدد السبب بدقة.",
        },
        "bsod_res_heatpower": {
            "title": "شاشة زرقاء تحت الضغط (Heat/Power)",
            "severity": "warn",
            "summary": "غالبًا حرارة أو مزود طاقة/شاحن غير كافي أو عدم استقرار.",
            "steps": [
                "افحص السخونة والتهوية (نفس خطوات السخونة).",
                "لو Desktop: تأكد من مزود الطاقة PSU مناسب وسليم.",
                "قلل الضغط مؤقتًا (خفض إعدادات الألعاب).",
                "حدّث تعريف كرت الشاشة.",
            ],
            "extra": "استمرارها قد يسبب فساد ملفات—يفضل حل السبب الأساسي بسرعة.",
        },
        "bsod_res_ramdisk": {
            "title": "شاشة زرقاء في الاستخدام العادي (RAM/Disk)",
            "severity": "warn",
            "summary": "السبب الشائع: رام غير مستقرة أو أخطاء قرص/ملفات نظام.",
            "steps": [
                "شغّل Windows Memory Diagnostic.",
                "افتح Command Prompt كمسؤول وشغّل: sfc /scannow",
                "تأكد من مساحة كافية على C.",
                "لو عندك HDD قديم: احتمال Bad sectors—اعمل Backup.",
            ],
            "extra": "لو المشكلة مستمرة، فحص SMART للهارد مفيد (بأداة موثوقة).",
        },
        "stor_res_cfull": {
            "title": "قرص C ممتلئ",
            "severity": "ok",
            "summary": "تفريغ C يحسن الأداء والتحديثات. ابدأ بالأمان: ملفات مؤقتة وتنزيلات.",
            "steps": [
                "Settings → System → Storage → Temporary files واحذف الآمن.",
                "انقل Downloads/Videos لقرص تاني.",
                "احذف البرامج الثقيلة غير الضرورية.",
                "فعّل Storage Sense للتنظيف الدوري.",
            ],
            "extra": "سيب 15–20GB فاضي على الأقل لتجنب مشاكل الأداء.",
        },
        "stor_res_other": {
            "title": "قرص بيانات ممتلئ",
            "severity": "ok",
            "summary": "حلها تنظيم/نقل/حذف أو إضافة مساحة.",
            "steps": [
                "رتّب الملفات حسب الحجم واحذف غير الضروري.",
                "انقل أرشيفات/فيديوهات لقرص خارجي.",
                "لو القرص ممتلئ دائمًا: فكّر في ترقية السعة.",
            ],
            "extra": "احتفظ بنسخة احتياطية قبل نقل كميات كبيرة.",
        },
        "io_res_usb": {
            "title": "USB كيبورد/ماوس",
            "severity": "ok",
            "summary": "غالبًا منفذ/تعريف/طاقة USB أو العتاد نفسه.",
            "steps": [
                "جرّب منفذ USB مختلف (يفضل خلفي للـ Desktop).",
                "جرّب الجهاز على كمبيوتر تاني للتأكد هل هو تالف.",
                "Restart للجهاز.",
                "افصل أي USB hubs وجرب مباشر.",
            ],
            "extra": "لو المشكلة بتظهر بعد Sleep، جرّب تعطيل USB selective suspend من Power options.",
        },
        "io_res_laptop": {
            "title": "كيبورد/تاتش باد اللاب",
            "severity": "warn",
            "summary": "ممكن تعريف/إعداد أو مشكلة هاردوير (فلاتة/سوائل).",
            "steps": [
                "Restart للجهاز.",
                "تأكد إن Touchpad مش متقفل (Fn key في بعض اللابات).",
                "حدّث تعريفات Touchpad/Keyboard من موقع الشركة.",
                "لو اتسكب سائل: اقفل الجهاز فورًا وجففه وافصل الكهرباء ثم فني.",
            ],
            "extra": "تعطل بعض الأزرار فقط قد يكون Dirt تحت الزر أو مشكلة لوحة مفاتيح.",
        },
    },
}


def option_target_to_result_if_needed():
    """
    Normalize: if option["next"] points to an existing result id, convert to option["result"].
    This mirrors the JS behavior but keeps KB clean for the server.
    """
    results = KB["results"]
    for node in KB["nodes"].values():
        for opt in node.get("options", []):
            nxt = opt.get("next")
            if nxt and nxt in results:
                opt["result"] = nxt
                opt.pop("next", None)


option_target_to_result_if_needed()

