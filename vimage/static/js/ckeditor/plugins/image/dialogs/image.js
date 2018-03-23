﻿/*
 Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
(function(){var g=function(c,e){function f(){var a=arguments,b=this.getContentElement("advanced","txtdlgGenStyle");b&&b.commit.apply(b,a);this.foreach(function(b){b.commit&&"txtdlgGenStyle"!=b.id&&b.commit.apply(b,a)})}function l(a){if(!u){u=1;var b=this.getDialog(),d=b.imageElement;if(d){this.commit(1,d);a=[].concat(a);for(var c=a.length,e,f=0;f<c;f++)(e=b.getContentElement.apply(b,a[f].split(":")))&&e.setup(1,d)}u=0}}var g=/^\s*(\d+)((px)|\%)?\s*$/i,x=/(^\s*(\d+)((px)|\%)?\s*$)|^$/i,q=/^\d+px$/,
y=function(){var a=this.getValue(),b=this.getDialog(),d=a.match(g);d&&("%"==d[2]&&m(b,!1),a=d[1]);b.lockRatio&&(d=b.originalElement,"true"==d.getCustomData("isReady")&&("txtHeight"==this.id?(a&&"0"!=a&&(a=Math.round(a/d.$.height*d.$.width)),isNaN(a)||b.setValueOf("info","txtWidth",a)):(a&&"0"!=a&&(a=Math.round(a/d.$.width*d.$.height)),isNaN(a)||b.setValueOf("info","txtHeight",a))));h(b)},h=function(a){if(!a.originalElement||!a.preview)return 1;a.commitContent(4,a.preview);return 0},u,m=function(a,
b){if(!a.getContentElement("info","ratioLock"))return null;var d=a.originalElement;if(!d)return null;if("check"==b){if(!a.userlockRatio&&"true"==d.getCustomData("isReady")){var c=a.getValueOf("info","txtWidth"),e=a.getValueOf("info","txtHeight"),d=1E3*d.$.width/d.$.height,f=1E3*c/e;a.lockRatio=!1;c||e?isNaN(d)||isNaN(f)||Math.round(d)!=Math.round(f)||(a.lockRatio=!0):a.lockRatio=!0}}else void 0!==b?a.lockRatio=b:(a.userlockRatio=1,a.lockRatio=!a.lockRatio);c=CKEDITOR.document.getById(r);a.lockRatio?
c.removeClass("cke_btn_unlocked"):c.addClass("cke_btn_unlocked");c.setAttribute("aria-checked",a.lockRatio);CKEDITOR.env.hc&&c.getChild(0).setHtml(a.lockRatio?CKEDITOR.env.ie?"■":"▣":CKEDITOR.env.ie?"□":"▢");return a.lockRatio},z=function(a,b){var d=a.originalElement;if("true"==d.getCustomData("isReady")){var c=a.getContentElement("info","txtWidth"),e=a.getContentElement("info","txtHeight"),f;b?d=f=0:(f=d.$.width,d=d.$.height);c&&c.setValue(f);e&&e.setValue(d)}h(a)},A=function(a,b){function d(a,b){var d=
a.match(g);return d?("%"==d[2]&&(d[1]+="%",m(c,!1)),d[1]):b}if(1==a){var c=this.getDialog(),e="",f="txtWidth"==this.id?"width":"height",h=b.getAttribute(f);h&&(e=d(h,e));e=d(b.getStyle(f),e);this.setValue(e)}},v,t=function(){var a=this.originalElement,b=CKEDITOR.document.getById(n);a.setCustomData("isReady","true");a.removeListener("load",t);a.removeListener("error",k);a.removeListener("abort",k);b&&b.setStyle("display","none");this.dontResetSize||z(this,!1===c.config.image_prefillDimensions);this.firstLoad&&
CKEDITOR.tools.setTimeout(function(){m(this,"check")},0,this);this.dontResetSize=this.firstLoad=!1;h(this)},k=function(){var a=this.originalElement,b=CKEDITOR.document.getById(n);a.removeListener("load",t);a.removeListener("error",k);a.removeListener("abort",k);a=CKEDITOR.getUrl(CKEDITOR.plugins.get("image").path+"images/noimage.png");this.preview&&this.preview.setAttribute("src",a);b&&b.setStyle("display","none");m(this,!1)},p=function(a){return CKEDITOR.tools.getNextId()+"_"+a},r=p("btnLockSizes"),
w=p("btnResetSize"),n=p("ImagePreviewLoader"),C=p("previewLink"),B=p("previewImage");return{title:c.lang.image["image"==e?"title":"titleButton"],minWidth:"moono-lisa"==(CKEDITOR.skinName||c.config.skin)?500:420,minHeight:360,onShow:function(){this.linkEditMode=this.imageEditMode=this.linkElement=this.imageElement=!1;this.lockRatio=!0;this.userlockRatio=0;this.dontResetSize=!1;this.firstLoad=!0;this.addLink=!1;var a=this.getParentEditor(),b=a.getSelection(),d=(b=b&&b.getSelectedElement())&&a.elementPath(b).contains("a",
1),c=CKEDITOR.document.getById(n);c&&c.setStyle("display","none");v=new CKEDITOR.dom.element("img",a.document);this.preview=CKEDITOR.document.getById(B);this.originalElement=a.document.createElement("img");this.originalElement.setAttribute("alt","");this.originalElement.setCustomData("isReady","false");d&&(this.linkElement=d,this.addLink=this.linkEditMode=!0,a=d.getChildren(),1==a.count()&&(c=a.getItem(0),c.type==CKEDITOR.NODE_ELEMENT&&(c.is("img")||c.is("input"))&&(this.imageElement=a.getItem(0),
this.imageElement.is("img")?this.imageEditMode="img":this.imageElement.is("input")&&(this.imageEditMode="input"))),"image"==e&&this.setupContent(2,d));if(this.customImageElement)this.imageEditMode="img",this.imageElement=this.customImageElement,delete this.customImageElement;else if(b&&"img"==b.getName()&&!b.data("cke-realelement")||b&&"input"==b.getName()&&"image"==b.getAttribute("type"))this.imageEditMode=b.getName(),this.imageElement=b;this.imageEditMode&&(this.cleanImageElement=this.imageElement,
this.imageElement=this.cleanImageElement.clone(!0,!0),this.setupContent(1,this.imageElement));m(this,!0);CKEDITOR.tools.trim(this.getValueOf("info","txtUrl"))||(this.preview.removeAttribute("src"),this.preview.setStyle("display","none"))},onOk:function(){if(this.imageEditMode){var a=this.imageEditMode;"image"==e&&"input"==a&&confirm(c.lang.image.button2Img)?(this.imageElement=c.document.createElement("img"),this.imageElement.setAttribute("alt",""),c.insertElement(this.imageElement)):"image"!=e&&"img"==
a&&confirm(c.lang.image.img2Button)?(this.imageElement=c.document.createElement("input"),this.imageElement.setAttributes({type:"image",alt:""}),c.insertElement(this.imageElement)):(this.imageElement=this.cleanImageElement,delete this.cleanImageElement)}else"image"==e?this.imageElement=c.document.createElement("img"):(this.imageElement=c.document.createElement("input"),this.imageElement.setAttribute("type","image")),this.imageElement.setAttribute("alt","");this.linkEditMode||(this.linkElement=c.document.createElement("a"));
this.commitContent(1,this.imageElement);this.commitContent(2,this.linkElement);this.imageElement.getAttribute("style")||this.imageElement.removeAttribute("style");this.imageEditMode?!this.linkEditMode&&this.addLink?(c.insertElement(this.linkElement),this.imageElement.appendTo(this.linkElement)):this.linkEditMode&&!this.addLink&&(c.getSelection().selectElement(this.linkElement),c.insertElement(this.imageElement)):this.addLink?this.linkEditMode?this.linkElement.equals(c.getSelection().getSelectedElement())?
(this.linkElement.setHtml(""),this.linkElement.append(this.imageElement,!1)):c.insertElement(this.imageElement):(c.insertElement(this.linkElement),this.linkElement.append(this.imageElement,!1)):c.insertElement(this.imageElement)},onLoad:function(){"image"!=e&&this.hidePage("Link");var a=this._.element.getDocument();this.getContentElement("info","ratioLock")&&(this.addFocusable(a.getById(w),5),this.addFocusable(a.getById(r),5));this.commitContent=f;"local"!==c.config.saveto?(this.hidePage("Upload"),
upload_domain=c.config.UploadDomain,bucket_domain=c.config.BucketDomain,plupload_flash_swf_url=c.config.PluploadFlashSwfUrl,savetocloud()):this.hidePage("QUpload")},onHide:function(){this.preview&&this.commitContent(8,this.preview);this.originalElement&&(this.originalElement.removeListener("load",t),this.originalElement.removeListener("error",k),this.originalElement.removeListener("abort",k),this.originalElement.remove(),this.originalElement=!1);delete this.imageElement},contents:[{id:"info",label:c.lang.image.infoTab,
accessKey:"I",elements:[{type:"vbox",padding:0,children:[{type:"hbox",widths:["280px","110px"],align:"right",className:"cke_dialog_image_url",children:[{id:"txtUrl",type:"text",label:c.lang.common.url,required:!0,onChange:function(){var a=this.getDialog(),b=this.getValue();if(0<b.length){var a=this.getDialog(),d=a.originalElement;a.preview&&a.preview.removeStyle("display");d.setCustomData("isReady","false");var c=CKEDITOR.document.getById(n);c&&c.setStyle("display","");d.on("load",t,a);d.on("error",
k,a);d.on("abort",k,a);d.setAttribute("src",b);a.preview&&(v.setAttribute("src",b),a.preview.setAttribute("src",v.$.src),h(a))}else a.preview&&(a.preview.removeAttribute("src"),a.preview.setStyle("display","none"))},setup:function(a,b){if(1==a){var d=b.data("cke-saved-src")||b.getAttribute("src");this.getDialog().dontResetSize=!0;this.setValue(d);this.setInitValue()}},commit:function(a,b){1==a&&(this.getValue()||this.isChanged())?(b.data("cke-saved-src",this.getValue()),b.setAttribute("src",this.getValue()),
c.config.lazyload&&(b.setAttribute(c.config.lazyloadAttribute,this.getValue()),b.setAttribute("class",c.config.lazyloadCss))):8==a&&(b.setAttribute("src",""),b.removeAttribute("src"))},validate:CKEDITOR.dialog.validate.notEmpty(c.lang.image.urlMissing)},{type:"button",id:"browse",style:"display:inline-block;margin-top:14px;",align:"center",label:c.lang.common.browseServer,hidden:!0,filebrowser:"info:txtUrl"}]}]},{id:"txtAlt",type:"text",label:c.lang.image.alt,accessKey:"T","default":"",onChange:function(){h(this.getDialog())},
setup:function(a,b){1==a&&this.setValue(b.getAttribute("alt"))},commit:function(a,b){1==a?(this.getValue()||this.isChanged())&&b.setAttribute("alt",this.getValue()):4==a?b.setAttribute("alt",this.getValue()):8==a&&b.removeAttribute("alt")}},{type:"hbox",children:[{id:"basic",type:"vbox",children:[{type:"hbox",requiredContent:"img{width,height}",widths:["50%","50%"],children:[{type:"vbox",padding:1,children:[{type:"text",width:"45px",id:"txtWidth",label:c.lang.common.width,onKeyUp:y,onChange:function(){l.call(this,
"advanced:txtdlgGenStyle")},validate:function(){var a=this.getValue().match(x);(a=!(!a||0===parseInt(a[1],10)))||alert(c.lang.common.invalidWidth);return a},setup:A,commit:function(a,b){var d=this.getValue();1==a?(d&&c.activeFilter.check("img{width,height}")?b.setStyle("width",CKEDITOR.tools.cssLength(d)):b.removeStyle("width"),b.removeAttribute("width")):4==a?d.match(g)?b.setStyle("width",CKEDITOR.tools.cssLength(d)):(d=this.getDialog().originalElement,"true"==d.getCustomData("isReady")&&b.setStyle("width",
d.$.width+"px")):8==a&&(b.removeAttribute("width"),b.removeStyle("width"))}},{type:"text",id:"txtHeight",width:"45px",label:c.lang.common.height,onKeyUp:y,onChange:function(){l.call(this,"advanced:txtdlgGenStyle")},validate:function(){var a=this.getValue().match(x);(a=!(!a||0===parseInt(a[1],10)))||alert(c.lang.common.invalidHeight);return a},setup:A,commit:function(a,b){var d=this.getValue();1==a?(d&&c.activeFilter.check("img{width,height}")?b.setStyle("height",CKEDITOR.tools.cssLength(d)):b.removeStyle("height"),
b.removeAttribute("height")):4==a?d.match(g)?b.setStyle("height",CKEDITOR.tools.cssLength(d)):(d=this.getDialog().originalElement,"true"==d.getCustomData("isReady")&&b.setStyle("height",d.$.height+"px")):8==a&&(b.removeAttribute("height"),b.removeStyle("height"))}}]},{id:"ratioLock",type:"html",className:"cke_dialog_image_ratiolock",style:"margin-top:30px;width:40px;height:40px;",onLoad:function(){var a=CKEDITOR.document.getById(w),b=CKEDITOR.document.getById(r);a&&(a.on("click",function(a){z(this);
a.data&&a.data.preventDefault()},this.getDialog()),a.on("mouseover",function(){this.addClass("cke_btn_over")},a),a.on("mouseout",function(){this.removeClass("cke_btn_over")},a));b&&(b.on("click",function(a){m(this);var b=this.originalElement,c=this.getValueOf("info","txtWidth");"true"==b.getCustomData("isReady")&&c&&(b=b.$.height/b.$.width*c,isNaN(b)||(this.setValueOf("info","txtHeight",Math.round(b)),h(this)));a.data&&a.data.preventDefault()},this.getDialog()),b.on("mouseover",function(){this.addClass("cke_btn_over")},
b),b.on("mouseout",function(){this.removeClass("cke_btn_over")},b))},html:'\x3cdiv\x3e\x3ca href\x3d"javascript:void(0)" tabindex\x3d"-1" title\x3d"'+c.lang.image.lockRatio+'" class\x3d"cke_btn_locked" id\x3d"'+r+'" role\x3d"checkbox"\x3e\x3cspan class\x3d"cke_icon"\x3e\x3c/span\x3e\x3cspan class\x3d"cke_label"\x3e'+c.lang.image.lockRatio+'\x3c/span\x3e\x3c/a\x3e\x3ca href\x3d"javascript:void(0)" tabindex\x3d"-1" title\x3d"'+c.lang.image.resetSize+'" class\x3d"cke_btn_reset" id\x3d"'+w+'" role\x3d"button"\x3e\x3cspan class\x3d"cke_label"\x3e'+
c.lang.image.resetSize+"\x3c/span\x3e\x3c/a\x3e\x3c/div\x3e"}]},{type:"vbox",padding:1,children:[{type:"text",id:"txtBorder",requiredContent:"img{border-width}",width:"60px",label:c.lang.image.border,"default":"",onKeyUp:function(){h(this.getDialog())},onChange:function(){l.call(this,"advanced:txtdlgGenStyle")},validate:CKEDITOR.dialog.validate.integer(c.lang.image.validateBorder),setup:function(a,b){if(1==a){var d;d=(d=(d=b.getStyle("border-width"))&&d.match(/^(\d+px)(?: \1 \1 \1)?$/))&&parseInt(d[1],
10);isNaN(parseInt(d,10))&&(d=b.getAttribute("border"));this.setValue(d)}},commit:function(a,b){var d=parseInt(this.getValue(),10);1==a||4==a?(isNaN(d)?!d&&this.isChanged()&&b.removeStyle("border"):(b.setStyle("border-width",CKEDITOR.tools.cssLength(d)),b.setStyle("border-style","solid")),1==a&&b.removeAttribute("border")):8==a&&(b.removeAttribute("border"),b.removeStyle("border-width"),b.removeStyle("border-style"),b.removeStyle("border-color"))}},{type:"text",id:"txtHSpace",requiredContent:"img{margin-left,margin-right}",
width:"60px",label:c.lang.image.hSpace,"default":"",onKeyUp:function(){h(this.getDialog())},onChange:function(){l.call(this,"advanced:txtdlgGenStyle")},validate:CKEDITOR.dialog.validate.integer(c.lang.image.validateHSpace),setup:function(a,b){if(1==a){var d,c;d=b.getStyle("margin-left");c=b.getStyle("margin-right");d=d&&d.match(q);c=c&&c.match(q);d=parseInt(d,10);c=parseInt(c,10);d=d==c&&d;isNaN(parseInt(d,10))&&(d=b.getAttribute("hspace"));this.setValue(d)}},commit:function(a,b){var d=parseInt(this.getValue(),
10);1==a||4==a?(isNaN(d)?!d&&this.isChanged()&&(b.removeStyle("margin-left"),b.removeStyle("margin-right")):(b.setStyle("margin-left",CKEDITOR.tools.cssLength(d)),b.setStyle("margin-right",CKEDITOR.tools.cssLength(d))),1==a&&b.removeAttribute("hspace")):8==a&&(b.removeAttribute("hspace"),b.removeStyle("margin-left"),b.removeStyle("margin-right"))}},{type:"text",id:"txtVSpace",requiredContent:"img{margin-top,margin-bottom}",width:"60px",label:c.lang.image.vSpace,"default":"",onKeyUp:function(){h(this.getDialog())},
onChange:function(){l.call(this,"advanced:txtdlgGenStyle")},validate:CKEDITOR.dialog.validate.integer(c.lang.image.validateVSpace),setup:function(a,b){if(1==a){var d,c;d=b.getStyle("margin-top");c=b.getStyle("margin-bottom");d=d&&d.match(q);c=c&&c.match(q);d=parseInt(d,10);c=parseInt(c,10);d=d==c&&d;isNaN(parseInt(d,10))&&(d=b.getAttribute("vspace"));this.setValue(d)}},commit:function(a,b){var d=parseInt(this.getValue(),10);1==a||4==a?(isNaN(d)?!d&&this.isChanged()&&(b.removeStyle("margin-top"),b.removeStyle("margin-bottom")):
(b.setStyle("margin-top",CKEDITOR.tools.cssLength(d)),b.setStyle("margin-bottom",CKEDITOR.tools.cssLength(d))),1==a&&b.removeAttribute("vspace")):8==a&&(b.removeAttribute("vspace"),b.removeStyle("margin-top"),b.removeStyle("margin-bottom"))}},{id:"cmbAlign",requiredContent:"img{float}",type:"select",widths:["35%","65%"],style:"width:90px",label:c.lang.common.align,"default":"",items:[[c.lang.common.notSet,""],[c.lang.common.alignLeft,"left"],[c.lang.common.alignRight,"right"]],onChange:function(){h(this.getDialog());
l.call(this,"advanced:txtdlgGenStyle")},setup:function(a,b){if(1==a){var d=b.getStyle("float");switch(d){case "inherit":case "none":d=""}!d&&(d=(b.getAttribute("align")||"").toLowerCase());this.setValue(d)}},commit:function(a,b){var d=this.getValue();if(1==a||4==a){if(d?b.setStyle("float",d):b.removeStyle("float"),1==a)switch(d=(b.getAttribute("align")||"").toLowerCase(),d){case "left":case "right":b.removeAttribute("align")}}else 8==a&&b.removeStyle("float")}}]}]},{type:"vbox",height:"250px",children:[{type:"html",
id:"htmlPreview",style:"width:95%;",html:"\x3cdiv\x3e"+CKEDITOR.tools.htmlEncode(c.lang.common.preview)+'\x3cbr\x3e\x3cdiv id\x3d"'+n+'" class\x3d"ImagePreviewLoader" style\x3d"display:none"\x3e\x3cdiv class\x3d"loading"\x3e\x26nbsp;\x3c/div\x3e\x3c/div\x3e\x3cdiv class\x3d"ImagePreviewBox"\x3e\x3ctable\x3e\x3ctr\x3e\x3ctd\x3e\x3ca href\x3d"javascript:void(0)" target\x3d"_blank" onclick\x3d"return false;" id\x3d"'+C+'"\x3e\x3cimg id\x3d"'+B+'" alt\x3d"" /\x3e\x3c/a\x3e'+(c.config.image_previewText||
"Image Preview. ")+"\x3c/td\x3e\x3c/tr\x3e\x3c/table\x3e\x3c/div\x3e\x3c/div\x3e"}]}]}]},{id:"Link",requiredContent:"a[href]",label:c.lang.image.linkTab,padding:0,elements:[{id:"txtUrl",type:"text",label:c.lang.common.url,style:"width: 100%","default":"",setup:function(a,b){if(2==a){var d=b.data("cke-saved-href");d||(d=b.getAttribute("href"));this.setValue(d)}},commit:function(a,b){if(2==a&&(this.getValue()||this.isChanged())){var d=this.getValue();b.data("cke-saved-href",d);b.setAttribute("href",
d);this.getValue()||!c.config.image_removeLinkByEmptyURL?this.getDialog().addLink=!0:this.getDialog().addLink=!1}}},{type:"button",id:"browse",className:"cke_dialog_image_browse",filebrowser:{action:"Browse",target:"Link:txtUrl",url:c.config.filebrowserImageBrowseLinkUrl},style:"float:right",hidden:!0,label:c.lang.common.browseServer},{id:"cmbTarget",type:"select",requiredContent:"a[target]",label:c.lang.common.target,"default":"",items:[[c.lang.common.notSet,""],[c.lang.common.targetNew,"_blank"],
[c.lang.common.targetTop,"_top"],[c.lang.common.targetSelf,"_self"],[c.lang.common.targetParent,"_parent"]],setup:function(a,b){2==a&&this.setValue(b.getAttribute("target")||"")},commit:function(a,b){2==a&&(this.getValue()||this.isChanged())&&b.setAttribute("target",this.getValue())}}]},{id:"Upload",hidden:!0,filebrowser:"uploadButton",label:c.lang.image.upload,elements:[{type:"file",id:"upload",label:c.lang.image.btnUpload,style:"height:40px",size:38},{type:"fileButton",id:"uploadButton",filebrowser:"info:txtUrl",
label:c.lang.image.btnUpload,"for":["Upload","upload"]}]},{id:"QUpload",hidden:!1,label:c.lang.image.upload,elements:[{type:"html",html:'\x3cdiv id\x3d"container"\x3e\x3cem id\x3d"fileinfo"\x3e\x3c/em\x3e\x3ca href\x3d"javascript:void(0)" id\x3d"setfile"\x3e[点击选择文件]\x3c/a\x3e\x3ca href\x3d"javascript:void(0)" id\x3d"uploadfile"\x3e[ 上传 ]\x3c/a\x3e\x3c/div\x3e'}]},{id:"advanced",label:c.lang.common.advancedTab,elements:[{type:"hbox",widths:["50%","25%","25%"],children:[{type:"text",id:"linkId",requiredContent:"img[id]",
label:c.lang.common.id,setup:function(a,b){1==a&&this.setValue(b.getAttribute("id"))},commit:function(a,b){1==a&&(this.getValue()||this.isChanged())&&b.setAttribute("id",this.getValue())}},{id:"cmbLangDir",type:"select",requiredContent:"img[dir]",style:"width : 100px;",label:c.lang.common.langDir,"default":"",items:[[c.lang.common.notSet,""],[c.lang.common.langDirLtr,"ltr"],[c.lang.common.langDirRtl,"rtl"]],setup:function(a,b){1==a&&this.setValue(b.getAttribute("dir"))},commit:function(a,b){1==a&&
(this.getValue()||this.isChanged())&&b.setAttribute("dir",this.getValue())}},{type:"text",id:"txtLangCode",requiredContent:"img[lang]",label:c.lang.common.langCode,"default":"",setup:function(a,b){1==a&&this.setValue(b.getAttribute("lang"))},commit:function(a,b){1==a&&(this.getValue()||this.isChanged())&&b.setAttribute("lang",this.getValue())}}]},{type:"text",id:"txtGenLongDescr",requiredContent:"img[longdesc]",label:c.lang.common.longDescr,setup:function(a,b){1==a&&this.setValue(b.getAttribute("longDesc"))},
commit:function(a,b){1==a&&(this.getValue()||this.isChanged())&&b.setAttribute("longDesc",this.getValue())}},{type:"hbox",widths:["50%","50%"],children:[{type:"text",id:"txtGenClass",requiredContent:"img(cke-xyz)",label:c.lang.common.cssClass,"default":"",setup:function(a,b){1==a&&this.setValue(b.getAttribute("class"))},commit:function(a,b){1==a&&(this.getValue()||this.isChanged())&&b.setAttribute("class",this.getValue())}},{type:"text",id:"txtGenTitle",requiredContent:"img[title]",label:c.lang.common.advisoryTitle,
"default":"",onChange:function(){h(this.getDialog())},setup:function(a,b){1==a&&this.setValue(b.getAttribute("title"))},commit:function(a,b){1==a?(this.getValue()||this.isChanged())&&b.setAttribute("title",this.getValue()):4==a?b.setAttribute("title",this.getValue()):8==a&&b.removeAttribute("title")}}]},{type:"text",id:"txtdlgGenStyle",requiredContent:"img{cke-xyz}",label:c.lang.common.cssStyle,validate:CKEDITOR.dialog.validate.inlineStyle(c.lang.common.invalidInlineStyle),"default":"",setup:function(a,
b){if(1==a){var d=b.getAttribute("style");!d&&b.$.style.cssText&&(d=b.$.style.cssText);this.setValue(d);var c=b.$.style.height,d=b.$.style.width,c=(c?c:"").match(g),d=(d?d:"").match(g);this.attributesInStyle={height:!!c,width:!!d}}},onChange:function(){l.call(this,"info:cmbFloat info:cmbAlign info:txtVSpace info:txtHSpace info:txtBorder info:txtWidth info:txtHeight".split(" "));h(this)},commit:function(a,b){1==a&&(this.getValue()||this.isChanged())&&b.setAttribute("style",this.getValue())}}]}]}};
CKEDITOR.dialog.add("image",function(c){return g(c,"image")});CKEDITOR.dialog.add("imagebutton",function(c){return g(c,"imagebutton")})})();
function savetocloud(){var g=new plupload.Uploader({runtimes:"html5,flash,html4",browse_button:"setfile",url:"",container:"container",max_file_size:"5120mb",filters:{mime_types:[{title:"Image files",extensions:"jpeg,jpg,gif,png,wbmp"}],prevent_duplicates:!0},flash_swf_url:window.plupload_flash_swf_url,max_retries:3,dragdrop:!0,drop_element:"container",chunk_size:"4mb",auto_start:!1,init:{PostInit:function(){document.getElementById("uploadfile").onclick=function(){g.start();return!1}},FilesAdded:function(c,
e){plupload.each(e,function(c){document.getElementById("fileinfo").innerHTML+='\x3cdiv id\x3d"'+c.id+'"\x3e'+c.name+"\x26nbsp;\x26nbsp;\x26nbsp;("+plupload.formatSize(c.size)+")\x26nbsp;\x26nbsp;\x26nbsp;\x26nbsp;\x26nbsp;\x26nbsp;\x3cb\x3e\x3c/b\x3e\t\x3ci\x3e\x3c/i\x3e\x3c/div\x3e\x3cbr\x3e"})},BeforeUpload:function(c,e){var f;time_ms=(new Date).getTime();"qiniu"==window.saveto?f={token:window.uptoken,key:window.time_ms+"_"+e.name}:"alioss"==window.saveto&&(f={key:window.path_key+window.time_ms+
"_"+e.name,policy:window.policyBase64,OSSAccessKeyId:window.accessid,success_action_status:"200",signature:window.signature});g.setOption({url:window.upload_domain,multipart_params:f})},UploadProgress:function(c,e){document.getElementById(e.id).getElementsByTagName("b")[0].innerHTML="\x3cspan\x3e"+e.percent+"%\x3c/span\x3e"},FileUploaded:function(c,e,f){c=JSON.parse(f.response);if("alioss"==window.saveto){if(200==f.status)var g=bucket_domain+"/"+window.path_key+window.time_ms+"_"+e.name}else g=bucket_domain+
"/"+c.key;document.getElementById(e.id).getElementsByTagName("i")[0].innerHTML=g;window.CKEDITOR.tools.callFunction(fnidnum,g,"ok")},Error:function(c,e,f){},UploadComplete:function(){}}});g.init()};