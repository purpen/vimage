﻿/*
 Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
(function(){CKEDITOR.plugins.add("stylescombo",{requires:"richcombo",lang:"af,ar,az,bg,bn,bs,ca,cs,cy,da,de,de-ch,el,en,en-au,en-ca,en-gb,eo,es,et,eu,fa,fi,fo,fr,fr-ca,gl,gu,he,hi,hr,hu,id,is,it,ja,ka,km,ko,ku,lt,lv,mk,mn,ms,nb,nl,no,oc,pl,pt,pt-br,ro,ru,si,sk,sl,sq,sr,sr-latn,sv,th,tr,tt,ug,uk,vi,zh,zh-cn",init:function(c){var l=c.config,g=c.lang.stylescombo,f={},k=[],m=[];c.on("stylesSet",function(b){if(b=b.data.styles){for(var a,h,d,e=0,n=b.length;e<n;e++)(a=b[e],c.blockless&&a.element in CKEDITOR.dtd.$block||
"string"==typeof a.type&&!CKEDITOR.style.customHandlers[a.type]||(h=a.name,a=new CKEDITOR.style(a),c.filter.customConfig&&!c.filter.check(a)))||(a._name=h,a._.enterMode=l.enterMode,a._.type=d=a.assignedTo||a.type,a._.weight=e+1E3*(d==CKEDITOR.STYLE_OBJECT?1:d==CKEDITOR.STYLE_BLOCK?2:3),f[h]=a,k.push(a),m.push(a));k.sort(function(a,b){return a._.weight-b._.weight})}});c.ui.addRichCombo("Styles",{label:g.label,title:g.panelTitle,toolbar:"styles,10",allowedContent:m,panel:{css:[CKEDITOR.skin.getPath("editor")].concat(l.contentsCss),
multiSelect:!0,attributes:{"aria-label":g.panelTitle}},init:function(){var b,a,c,d,e,f;e=0;for(f=k.length;e<f;e++)b=k[e],a=b._name,d=b._.type,d!=c&&(this.startGroup(g["panelTitle"+String(d)]),c=d),this.add(a,b.type==CKEDITOR.STYLE_OBJECT?a:b.buildPreview(),a);this.commit()},onClick:function(b){c.focus();c.fire("saveSnapshot");b=f[b];var a=c.elementPath();if(b.group&&b.removeStylesFromSameGroup(c))c.applyStyle(b);else c[b.checkActive(a,c)?"removeStyle":"applyStyle"](b);c.fire("saveSnapshot")},onRender:function(){c.on("selectionChange",
function(b){var a=this.getValue();b=b.data.path.elements;for(var h=0,d=b.length,e;h<d;h++){e=b[h];for(var g in f)if(f[g].checkElementRemovable(e,!0,c)){g!=a&&this.setValue(g);return}}this.setValue("")},this)},onOpen:function(){var b=c.getSelection().getSelectedElement(),b=c.elementPath(b),a=[0,0,0,0];this.showAll();this.unmarkAll();for(var h in f){var d=f[h],e=d._.type;d.checkApplicable(b,c,c.activeFilter)?a[e]++:this.hideItem(h);d.checkActive(b,c)&&this.mark(h)}a[CKEDITOR.STYLE_BLOCK]||this.hideGroup(g["panelTitle"+
String(CKEDITOR.STYLE_BLOCK)]);a[CKEDITOR.STYLE_INLINE]||this.hideGroup(g["panelTitle"+String(CKEDITOR.STYLE_INLINE)]);a[CKEDITOR.STYLE_OBJECT]||this.hideGroup(g["panelTitle"+String(CKEDITOR.STYLE_OBJECT)])},refresh:function(){var b=c.elementPath();if(b){for(var a in f)if(f[a].checkApplicable(b,c,c.activeFilter))return;this.setState(CKEDITOR.TRISTATE_DISABLED)}},reset:function(){f={};k=[]}})}})})();