# CSS OpenType字体特性

## 知识卡片

{{知识点1}}{{OpenType字体特性概述：OpenType字体格式支持丰富的排版特性（font features），包括连字（ligatures）、数字样式（numeric styles）、字母替换（alternates）等。CSS通过font-variant属性族和font-feature-settings属性来控制这些特性，使网页排版达到专业印刷水准。}}

{{知识点2}}{{font-variant属性：font-variant是控制OpenType特性的主要CSS简写属性，包含子属性：font-variant-ligatures（连字）、font-variant-caps（大写字母变体）、font-variant-numeric（数字样式）、font-variant-alternates（字形替换）、font-variant-east-asian（东亚文字变体）、font-variant-position（位置变体）和font-variant-emoji。}}

{{知识点3}}{{font-kerning属性：控制字偶间距（kerning），即特定字符对之间的间距调整。取值为auto（浏览器默认，通常开启）、normal（强制开启）和none（关闭）。OpenType规范建议默认开启kerning。注意letter-spacing会在kerning之后应用。}}

{{知识点4}}{{连字（Ligatures）：连字是将两个或多个字符组合成一个更美观字形的排版特性。常见连字包括fi、fl、ffl等。font-variant-ligatures属性控制连字行为，可设置common-ligatures（常用连字）、discretionary-ligatures（可选连字）、historical-ligatures（历史连字）和contextual（上下文替换）。}}

{{知识点5}}{{font-feature-settings属性：这是底层的OpenType特性控制属性，使用4字符的OpenType特性标签（如"kern"、"liga"、"dlig"）来启用或禁用特定特性。语法为font-feature-settings: "tag" value，其中value为1启用、0禁用。推荐优先使用font-variant高级属性，仅在需要细粒度控制时使用font-feature-settings。}}

{{知识点6}}{{大写字母变体（font-variant-caps）：提供多种大写字母样式选项。small-caps将小写字母显示为小型大写字母；all-small-caps将所有字母显示为小型大写；petite-caps和all-petite-caps使用更小的大写字母；unicase混合大小写形式；titling-caps用于标题的大写字母变体。}}

{{知识点7}}{{数字样式（font-variant-numeric）：控制数字的显示方式。lining-nums使用等高数字，oldstyle-nums使用旧式数字（部分数字有降部），proportional-nums使用比例宽度数字，tabular-nums使用等宽数字（适合表格对齐），diagonal-fractions使用对角线分数，stacked-fractions使用堆叠分数，slashed-zero给零加斜线以区分字母O。}}

{{知识点8}}{{字形替换（font-variant-alternates）：允许激活字体中提供的替代字形。可使用stylistic()激活单个样式集、styleset()激活命名样式集、character-variant()激活字符变体、swash()激活装饰性字形、ornaments()激活装饰符号、annotation()激活注解形式。需要配合@font-feature-values规则定义命名值。}}

{{知识点9}}{{@font-feature-values规则：用于为特定字体族定义命名的特性值，便于在font-variant-alternates中引用。语法为@font-feature-values "FontName" { @styleset { name: value; } }。可定义的规则包括@styleset、@stylistic、@character-variant、@swash、@ornaments、@annotation等。}}

{{知识点10}}{{东亚文字变体（font-variant-east-asian）：控制中日韩文字的字形变体。支持jis78/jis83/jis90/jis04（日文JIS标准变体）、simplified/traditional（简繁体变体）、full-width/proportional-width（全角/比例宽度）和ruby（注音标记形式）。对中文排版特别重要，可控制使用哪种字形标准。}}

{{知识点11}}{{font-variant-position属性：控制上标和下标文本的显示方式。sub将文本显示为下标形式，super将文本显示为上标形式。与HTML的sub/sup元素不同，此属性直接使用字体中的上下标字形，保持字体设计的一致性，而非通过缩放实现。}}

{{知识点12}}{{font-variant-emoji属性：控制emoji字符的显示样式。text强制以文本形式显示emoji，emoji强制以emoji彩色形式显示，unicode让浏览器根据Unicode标准的Emoji_Presentation属性自动决定显示形式。}}

{{知识点13}}{{字体特性发现工具：wakamaifondue.com可以上传字体文件并生成完整的OpenType特性报告；axis-praxis.org提供交互式特性测试，可点击开关各种特性查看效果。这些工具帮助开发者了解字体支持哪些高级排版特性。}}

{{知识点14}}{{CSS字体加载API：使用FontFace和FontFaceSet接口可以异步加载字体并监听加载事件。FontFace对象的featureSettings属性可设置OpenType特性。CSS.fonts.ready返回Promise，表示所有已声明字体加载完成。}}

{{知识点15}}{{字体特性与可访问性：正确使用OpenType特性可以提升文本可读性。连字使文本更平滑，旧式数字在正文中更自然，tabular-nums在数据表格中对齐更好，slashed-zero帮助区分0和O。但应避免过度使用可选连字（discretionary-ligatures），因为它们可能降低可读性。}}
