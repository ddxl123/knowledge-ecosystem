# CSS Font字体

## 知识卡片

{{知识点1}}{{CSS字体系统概述：CSS字体系统包括字体族选择（font-family）、字体大小（font-size）、字体粗细（font-weight）、字体样式（font-style）、字体拉伸（font-stretch）等核心属性。CSS Fonts模块还定义了@font-face规则用于加载自定义字体，以及可变字体（Variable Fonts）等现代特性。}}

{{知识点2}}{{font-family属性：指定字体族名称或通用字体族。可列出多个字体作为备选（fallback），用逗号分隔。通用字体族包括serif（衬线）、sans-serif（无衬线）、monospace（等宽）、cursive（手写）、fantasy（装饰）。包含空格的字体名需要引号包裹。浏览器使用第一个可用字体。}}

{{知识点3}}{{font-size属性：设置字体大小。可使用绝对值（xx-small、x-small、small、medium、large、x-large、xx-large）、相对值（larger、smaller）、长度值（px、em、rem、vw等）或百分比（相对于父元素字体大小）。推荐使用rem作为基础单位以实现一致的缩放行为。}}

{{知识点4}}{{font-weight属性：设置字体粗细。可使用关键字（normal=400、bold=700、lighter、bolder）或100-900的整数值（以100为步长）。lighter和bolder相对于父元素的粗细进行计算。可变字体支持1-1000范围内的任意值，实现更精细的粗细控制。}}

{{知识点5}}{{font-style属性：设置字体样式。normal为正常体，italic为斜体（使用字体的真正斜体设计），oblique为倾斜体（通过算法倾斜正常体）。oblique可指定倾斜角度（如oblique 14deg），可变字体支持-90deg到90deg的角度范围。italic通常比oblique有更好的设计质量。}}

{{知识点6}}{{font-stretch属性：设置字体的拉伸程度。可使用关键字（ultra-condensed、extra-condensed、condensed、semi-condensed、normal、semi-expanded、expanded、extra-expanded、ultra-expanded）或百分比值（50%-200%）。只影响支持宽度变体的字体族。CSS Fonts Level 4将此属性更名为font-width。}}

{{知识点7}}{{font简写属性：font属性是多个字体属性的简写形式，顺序为font-style font-variant font-weight font-stretch font-size/line-height font-family。font-size和font-family是必需的，其他可选。font-variant只能使用normal或small-caps。简写会将未指定的属性重置为初始值。}}

{{知识点8}}{{@font-face规则：用于从外部加载字体。基本语法包含font-family（字体名称）、src（字体文件路径和格式）、font-weight、font-style、font-stretch等描述符。src可列出多个格式（如woff2、woff、truetype）供浏览器选择，使用format()提示格式。}}

{{知识点9}}{{字体加载策略：@font-face的font-display属性控制字体加载期间的显示策略。auto使用浏览器默认行为，block先显示不可见文本（最多3秒），swap先显示后备字体后替换（可变字体推荐），fallback短暂隐藏（100ms）后使用后备字体，optional在慢网络下可能直接使用后备字体。}}

{{知识点10}}{{可变字体（Variable Fonts）：可变字体在一个文件中包含完整的字体设计空间，通过轴（axis）参数动态调整属性。标准轴包括wght（粗细，对应font-weight）、wdth（宽度，对应font-stretch）、ital（斜体）、slnt（倾斜）和opsz（光学大小）。使用font-variation-settings属性或标准CSS属性控制。}}

{{知识点11}}{{font-variation-settings属性：直接控制可变字体的轴值。语法为font-variation-settings: "axis_tag" value。例如font-variation-settings: "wght" 450, "wdth" 85。自定义轴使用4字符标签（大写字母开头）。建议优先使用标准CSS属性（font-weight等），仅在需要非标准轴时使用font-variation-settings。}}

{{知识点12}}{{font-optical-sizing属性：控制是否启用光学大小调整。auto让浏览器根据字体大小自动调整字形细节，none禁用光学大小调整。光学大小调整使小字号文本的笔画更粗、字怀更大以提高可读性，大字号文本的细节更精致。需要字体支持opsz轴。}}

{{知识点13}}{{字体加载API：FontFace接口用于编程方式加载字体。new FontFace('name', 'url(font.woff2)')创建字体对象，fontFace.load()返回Promise。document.fonts.add(fontFace)将字体添加到文档。FontFaceSet接口（document.fonts）提供字体集合操作和ready属性。}}

{{知识点14}}{{font-size-adjust属性：当首选字体不可用时，调整后备字体的x高度（x-height）以保持视觉一致性。值为x高度与字体大小的比率。计算公式为：调整后大小 = font-size × (font-size-adjust / 后备字体的aspect value)。确保不同字体间的可读性一致。}}

{{知识点15}}{{font-synthesis属性：控制浏览器是否自动合成缺失的字体变体。none禁用所有合成，weight允许合成粗体，style允许合成斜体，small-caps允许合成小型大写字母。当字体没有真正的粗体或斜体设计时，浏览器会通过算法合成，但这可能导致视觉质量下降。}}

{{知识点16}}{{system-ui字体族：system-ui是一个通用字体族关键字，表示操作系统的默认UI字体。在macOS上通常是San Francisco，Windows上是Segoe UI，Android上是Roboto。使用font-family: system-ui可以快速匹配系统原生外观。}}

{{知识点17}}{{emoji字体族：emoji是一个通用字体族关键字，专门用于emoji字符的渲染。确保emoji使用彩色字体而非文本形式显示。常用设置为font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", emoji以覆盖各平台。}}

{{知识点18}}{{math字体族：math是一个通用字体族关键字，用于数学公式排版。适用于数学符号、上下标、分数等数学排版场景。结合HTML的math元素和MathML使用，确保数学表达式的正确渲染。}}

{{知识点19}}{{cursive字体族：cursive是一个通用字体族关键字，表示手写或草书字体。不同浏览器和操作系统映射到不同的实际字体。通常用于装饰性文本或模拟手写效果，不适合正文阅读。}}

{{知识点20}}{{fantasy字体族：fantasy是一个通用字体族关键字，表示装饰性或艺术字体。通常用于标题、广告或特殊设计场景。包含Comic Sans MS、Papyrus等装饰性字体。不建议用于正文或需要高可读性的场景。}}

{{知识点21}}{{monospace字体族：monospace是一个通用字体族关键字，表示等宽字体。所有字符占用相同宽度，适合代码显示、终端模拟器、ASCII艺术等场景。常用等宽字体包括Consolas、Monaco、Courier New、Source Code Pro等。}}

{{知识点22}}{{本地字体引用：@font-face的src描述符支持local()函数引用用户系统中已安装的字体。优先使用local()可以避免不必要的网络请求。例如src: local("Helvetica Neue"), url("helvetica-neue.woff2") format("woff2")。但不同操作系统的字体名称可能不同，需要谨慎处理。}}

{{知识点23}}{{字体格式与兼容性：常用字体格式包括WOFF2（最佳压缩，现代浏览器支持）、WOFF（广泛支持）、TTF/OTF（原始格式）、EOT（仅IE支持，已过时）、SVG（已废弃）。推荐优先使用WOFF2，配合WOFF作为后备。}}

{{知识点24}}{{unicode-range描述符：@font-face的unicode-range指定该字体文件包含的Unicode字符范围。浏览器仅在页面中存在匹配字符时才下载字体文件，优化加载性能。例如unicode-range: U+0000-00FF指定基本拉丁字符集。常用于字体子集化。}}

{{知识点25}}{{font-language-override属性：覆盖字体默认的语言系统。某些字体对不同语言使用不同的字形（如塞尔维亚语和俄语的西里尔字母形状不同）。设置font-language-override: "SRB"可强制使用塞尔维亚语的字形。值为ISO 639语言代码。}}

{{知识点26}}{{size-adjust描述符：@font-face的size-adjust描述符（CSS Fonts Level 4）类似于font-size-adjust，但在@font-face级别调整。用于调整后备字体的大小以匹配首选字体，确保字体切换时布局不跳动。值为百分比，默认100%。}}

{{知识点27}}{{ascent-override、descent-override、line-gap-override描述符：这些@font-face描述符（CSS Fonts Level 4）允许覆盖字体的上升高度、下降高度和行间距。用于精确控制后备字体的行高行为，确保字体切换时行间距保持一致。}}

{{知识点28}}{{font-palette属性（CSS Fonts Level 4）：用于选择彩色字体（COLR/CPAL）的调色板。可使用light或dark关键字选择亮色或暗色主题调色板，或使用@font-palette-values规则自定义调色板。对支持彩色字体的图标字体和装饰字体特别有用。}}

{{知识点29}}{{@font-palette-values规则：自定义彩色字体的调色板。语法为@font-palette-values --name { font-family: "FontName"; base-palette: light; override-color: 0 #ff0000; }。可以基于现有调色板覆盖特定颜色索引，实现主题切换和品牌定制。}}

{{知识点30}}{{字体加载性能优化：使用font-display:swap确保文本始终可见；使用preload提前加载关键字体（<link rel="preload" as="font">）；使用unicode-range实现按需加载；使用WOFF2格式减小文件大小；考虑使用system-ui避免网络加载；使用font-synthesis: none避免不必要的字体合成。}}
