/**
 * Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {

	config.extraPlugins = 'uploadimage,filebrowser';
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';

	// Save images to Qiniu or Ali OSS. If seted saveto, must be set: BucketDomain
	config.saveto = 'qiniu';
	config.BucketDomain = 'https://kg.erp.taihuoniao.com';
	config.UploadDomain = 'https://up.qbox.me';
	config.PluploadFlashSwfUrl = '/plupload_flash_swf.swf';

	// Images use lazyload. If seted lazyload, must be set: lazyloadattribute, config.extraAllowedContent
	// config.lazyload = true;
	config.lazyloadImg = '/skin/images/logo.png';
	config.lazyloadAttribute = 'data-original';
	config.lazyloadCss = 'lazy';
	config.extraAllowedContent = 'img[data-original]';

	config.autoParagraph = false;
	config.enterMode = CKEDITOR.ENTER_BR;
	config.shiftEnterMode = CKEDITOR.ENTER_P;

	config.removeButtons = 'Cut,Copy,Italic,Underline,Subscript,Superscript,JustifyBlock,Anchor';
};

