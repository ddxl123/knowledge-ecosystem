# CSS Text文本处理

## 知识卡片

{{知识点1}}{{CSS Text模块概述：CSS Text模块定义了文本操作相关的属性，包括换行、对齐、空白处理和文本转换。主要规范为CSS Text Module Level 3和Level 4。该模块控制文本在容器中的排列和断行行为，是网页排版的核心模块之一。}}

{{知识点2}}{{text-align属性：控制行内内容的水平对齐方式。取值包括left（左对齐）、right（右对齐）、center（居中）、justify（两端对齐）、start（根据书写方向对齐起始端）、end（根据书写方向对齐末端）。默认值为start，推荐使用逻辑值start/end而非物理值left/right以支持多语言布局。}}

{{知识点3}}{{text-align-last属性：控制多行文本最后一行的对齐方式。取值与text-align类似（auto、left、right、center、justify、start、end）。auto值使最后一行跟随text-align的设置。在使用justify两端对齐时，通常希望最后一行左对齐或start对齐。}}

{{知识点4}}{{text-indent属性：控制文本块首行的缩进量。可使用长度值（如2em）或百分比值（相对于包含块宽度）。支持each-line关键字（每个多行块的首行都缩进）和hanging关键字（反转缩进方向，实现悬挂缩进效果）。}}

{{知识点5}}{{text-transform属性：控制文本的大小写转换。none不转换，capitalize将每个单词首字母大写，uppercase全部转大写，lowercase全部转小写，full-width将所有字符转换为等宽形式（适合东亚排版），full-size-kana将小假名转为正常大小。}}

{{知识点6}}{{letter-spacing属性：控制字符之间的额外间距。正值增加间距，负值减少间距。可使用长度值或normal（默认值，使用字体的默认字距）。注意letter-spacing在kerning之后应用，每行最后一个字符后也会添加间距。}}

{{知识点7}}{{word-spacing属性：控制单词之间的额外间距。正值增加间距，负值减少间距。可使用长度值或normal（默认值，通常为0）。百分比值相对于受影响字符的字形advance width（前进宽度）计算。}}

{{知识点8}}{{white-space属性：控制空白字符（空格、制表符、换行符）的处理方式。normal合并空白并自动换行，nowrap合并空白但不换行，pre保留空白不换行（类似pre元素），pre-wrap保留空白并自动换行，pre-line合并空白但保留换行符并自动换行。break-spaces类似pre-wrap但会在保留的空白后允许换行。}}

{{知识点9}}{{white-space-collapse属性（CSS Text Level 4）：将white-space的空白折叠行为独立为单独属性。collapse合并连续空白，preserve保留所有空白，breaks保留换行符但合并空格，preserve-breaks保留换行符并合并空格，discard丢弃所有空白。}}

{{知识点10}}{{text-wrap属性（CSS Text Level 4）：简写属性，包含text-wrap-mode和text-wrap-style。text-wrap-mode控制是否换行（wrap或nowrap），text-wrap-style控制换行算法（auto、balance、pretty、stable）。balance值会尝试使多行文本的行长尽可能均衡。}}

{{知识点11}}{{text-wrap-style的balance值：尝试平衡多行文本的行长，使每行长度尽量接近。适用于标题和短文本块。pretty值使用更精细的排版算法优化换行，避免寡行（orphan）和孤行（widow）。stable值确保在编辑过程中文本换行位置不会频繁变化，适合可编辑内容。}}

{{知识点12}}{{overflow-wrap属性：控制当单词太长无法在一行内显示时的处理方式。normal使用默认换行规则，anywhere允许在任意字符处断行（且该断点参与最小内容宽度计算），break-word允许在任意字符处断行（但不影响最小内容宽度计算）。anywhere和break-word都会覆盖word-break的normal规则。}}

{{知识点13}}{{word-break属性：控制单词的断行规则。normal使用默认断行规则，break-all允许在任意字符间断行（适合CJK文本与拉丁文本混排），keep-all禁止CJK文本中的断行。注意word-break:break-all与overflow-wrap:break-word的区别：break-all总是在行尾断行，break-word仅在无法正常换行时才在任意位置断行。}}

{{知识点14}}{{hyphens属性：控制自动连字符断行。none禁止自动连字符，manual仅在文本中手动指定的断点处添加连字符（使用软连字符­），auto允许浏览器根据语言规则自动添加连字符断行。需要配合lang属性使用，浏览器根据语言规则决定断词和连字符位置。}}

{{知识点15}}{{line-break属性：控制CJK文本的断行严格程度。auto使用默认规则，loose使用最宽松的规则（适合短行文本），normal使用正常规则，strict使用最严格的规则（避免在某些标点符号处断行）。strict模式下，某些标点符号（如破折号、省略号）前后不会断行。}}

{{知识点16}}{{writing-mode属性：控制文本的书写方向。horizontal-tb从左到右、从上到下（默认），vertical-rl从上到下、从右到左（传统中文/日文竖排），vertical-lr从上到下、从左到右。writing-mode会影响文本流方向和块级元素的排列方向。}}

{{知识点17}}{{direction属性：设置文本的书写方向。ltr为从左到右（默认），rtl为从右到左（阿拉伯语、希伯来语等）。推荐使用HTML的dir属性而非CSS的direction属性，因为dir属性具有语义意义且影响Unicode双向算法。unicode-bidi属性配合direction控制双向文本的嵌入和覆盖行为。}}

{{知识点18}}{{text-overflow属性：控制溢出文本的视觉表示。clip直接裁剪溢出内容，ellipsis使用省略号（…）表示溢出内容。生效条件：元素必须有overflow:hidden、white-space:nowrap，且内容在块方向上有溢出。省略号仅在块末尾显示，不支持多行省略。}}

{{知识点19}}{{hanging-punctuation属性：控制标点符号是否悬挂到文本块的起始或结束边缘。first将块首的标点悬挂，last将块尾的标点悬挂，force-end强制悬挂行尾标点，allow-end允许行尾标点悬挂。悬挂标点可以使文本块的边缘看起来更整齐，是专业排版的常见做法。}}

{{知识点20}}{{tab-size属性：控制制表符（Tab）字符的显示宽度。可使用整数（表示空格数，默认为8）或长度值。配合white-space:pre使用时，可以控制代码块中制表符的显示宽度。现代浏览器支持长度值，可以更精确地控制制表符宽度。}}

{{知识点21}}{{text-autospace属性（CSS Text Level 4）：控制CJK文本与非CJK文本（如拉丁字母、数字）之间的额外间距。取值包括no-autospace（不添加额外间距）、ideograph-alpha（在表意文字和字母之间添加）、ideograph-numeric（在表意文字和数字之间添加）等。对中英文混排排版质量至关重要。}}

{{知识点22}}{{text-spacing-trim属性（CSS Text Level 4）：控制CJK标点符号的间距修剪。space-all保留所有标点间距，space-first仅保留行首标点间距，trim-start修剪行首标点间距，normal根据排版习惯自动处理。可使标点符号更紧凑，达到专业中文排版效果。}}

{{知识点23}}{{min-content和max-content关键字：用于width、min-width、max-width等属性。min-content是内容能占用的最小宽度（在不溢出的情况下，通常是最长单词的宽度），max-content是内容不换行时的自然宽度。这些值基于内容的内在尺寸计算。}}

{{知识点24}}{{break-inside、break-before、break-after属性：控制分页/分列时的断行行为。break-inside:avoid避免元素内部断行，break-before:page在元素前强制分页，break-after:column在元素后强制分列。auto让浏览器自行决定断点。对打印样式和多列布局特别重要。}}

{{知识点25}}{{orphans和widows属性：控制分页时页面底部和顶部的最小行数。orphans设置页面底部必须保留的最小行数（默认为2），widows设置新页面顶部必须保留的最小行数（默认为2）。防止标题出现在页面底部而正文在下一页的情况。}}
