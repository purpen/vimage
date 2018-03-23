/*
 * mixpus 自定义库
 * @author mic
 */
var mixpus = {
	author: 'mic',
	csrf_token: '',
	language: 'en',
	// 本地化语言标签
	locale: {
		locale_label: '',
		copy_ok_message: ''
	},
	urls: {
		show_assets: ''
	},
	lodop: '', // 网络打印机实例
	container_id: '#pjax-container',
	img_last_open_folder: '', // 缓存最近的上传目录
	show_ok_message: function (message) {
		swal({
		 	title: message,
			text: null,
			type: 'success',
			confirmButtonText: 'Ok',
			confirmButtonColor: '#008749'
		 });
	},
	show_warning_message: function (message) {
		swal({
		 	title: 'Warning!',
			text: message,
			type: 'info',
			confirmButtonText: 'Yes, I Got!',
			confirmButtonColor: '#faa937'
		 });
	},
	show_error_message: function (message) {
		 swal({
		 	title: 'Error!',
			text: message,
			type: 'error',
			confirmButtonText: 'Yes, I Got!',
			confirmButtonColor: '#c6322a'
		 });
	},
	// CLodop网络打印机地址设置
	c_lodop_hosts: 'localhost:8000,localhost:18000',
	version: 1.0
};

mixpus.init_page_layout = function () {

	$(document).ajaxStart(function () {
		NProgress.start();
	});

	$(document).ajaxStop(function () {
		//加载进度条完成。
		NProgress.done();

		$(mixpus.container_id).stop(true, true).fadeIn();
	});

	$('.alert-success.alert-dismissable').fadeTo(2000, 500).fadeOut(500, function(){
		$('.alert-dismissable').alert('close');
		$('.flashes').fadeOut(500, function () {
			$(this).remove();
		});
	});

	mixpus.hook_popover_toggle();

	mixpus.hook_select2();

	mixpus.hook_tooltip_toggle();

	mixpus.hook_all_check();

	mixpus.hook_ajax_modal();

	mixpus.hook_delete_all();

	mixpus.hook_form_datetime();

	// 复制到剪贴板
	var clipboard = new Clipboard('.zclip');
	clipboard.on('success', function(e) {
		e.clearSelection();
		mixpus.show_ok_message(mixpus.locale.copy_ok_message);
	});
	clipboard.on('error', function(e) {
		console.error('Action:', e.action);
		console.error('Trigger:', e.trigger);
	});

};

// 窗口变化
mixpus.hook_window_resize = function () {
	var min_height = $(window).height() - 50; // 减去导航条高度

	$('.content-wrapper > .content').css({'min-height': min_height});
};

mixpus.hook_select2 = function () {
	$('.select2').each(function (i, obj) {
		if (!$(obj).data("select2")) {
			$(obj).select2({
				'width': '100%'
			});
		}
	});
};

mixpus.hook_tooltip_toggle = function () {
	$('[data-toggle="tooltip"]').tooltip({
		container: 'body',
		trigger: 'hover',
		html: true
	});
};

mixpus.hook_popover_toggle = function () {
	$("a[rel=popover]")
		.popover({
      		'html': true,
			'placement': 'top'
	  	})
      	.click(function(e) {
      		e.preventDefault()
      	});
};

mixpus.hook_form_datetime = function () {
	$(".form-datetime").datetimepicker({
		minView: "month",
		language: mixpus.language,
		format: "yyyy-mm-dd",
		icons: {
			time: 'fa fa-time',
			date: 'fa fa-calendar',
			up: 'fa fa-chevron-up',
			down: 'fa fa-chevron-down'
		},
		autoclose: true,
		todayBtn: true
	});

	$('.form-date span.input-group-addon').click(function () {
		$(this).prev('.form-datetime').focus();
	});
};

mixpus.trim = function (str) {
	return str.replace(/^\s+|\s+$/g, "");
};

mixpus.check_is_install = function () {
	try{
		var LODOP = getLodop();
		if (LODOP.VERSION) {
			if (LODOP.CVERSION) {
				alert("当前有C-Lodop云打印可用!\n C-Lodop版本:"+LODOP.CVERSION+"(内含Lodop"+LODOP.VERSION+")");
			} else {
				alert("本机已成功安装了Lodop控件！\n 版本号:"+LODOP.VERSION);
			}
		};
	}catch(err){}
};

mixpus.hook_pjax_link = function () {
	// 导航菜单链接
	$.pjax({
		selector: 'a.pjax',
		container: mixpus.container_id, //内容替换的容器
		show: 'fade',  //展现的动画，支持默认和fade, 可以自定义动画方式，这里为自定义的function即可。
		cache: false,  //是否使用缓存
		storage: false,  //是否使用本地存储
		title: '小灵兽',
		titleSuffix: ' - Free Cloud Based ERP Solution', //标题后缀
		filter: function(){},
		callback: function(status){
			var type = status.type;
			switch (type) {
				case 'success':
					$(this)
						.parents('.sidebar')
						.find('a.pjax.active').removeClass('active')
						.end()
						.end()
						.addClass('active');
					break;
				case 'error':
					break; //发生异常
			}
		}
	});

	$(document).on('pjax:start', function () {
		NProgress.start();
	});

	$(document).on('pjax:end', function () {
		//加载进度条完成。
		NProgress.done();
		$(mixpus.container_id).stop(true, true).fadeIn();
	});
};

mixpus.display_alert = function (messages) {
	var html = '<div class="alert alert-warning alert-dismissible fade in" role="alert"> ';
	html += '<button class="close" type="button" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>';
	
	for (var i=0; i<messages.length; i++) {
		html += '<p><strong>'+ messages[i]['field'] +':</strong> '+ messages[i]['message'] +'</p>';
	}
	
	html += '</div>';

	return html
};

mixpus.get_url_params = function (href) {
	href = href.split('?');
	href.shift();
	href = href.join('?');
	href = href.split('&');
	var query = {};
	for (var i=0; i<href.length; i+=1) {
		var q = href[i].split('=');
		query[q[0]] = q[1];
	}
	return query;
};

mixpus.hook_dropdown_menu = function (callback) {
	$('.dropdown-select-menu .option').on('click', function (cb) {
		var $this=$(this), label=$(this).text(), v=$(this).data('id'),
			target=$(this).parent().parent().data('target');

		$(this)
			.parent()
			.siblings('.active').removeClass('active')
			.end()
			.addClass('active');

		$('input[name='+ target +']').val(v);

		$(this).parent().parent().prev().find('b').text(label);

		callback && callback.call(this);
	});
};

mixpus.hook_filter_search = function (callback) {
	$('input.searcher').on('keydown', function (e) {
		var ev = window.event||e;
		if (ev.keyCode == 13) {
			callback && callback.call();
			return false;
		}
	});
};

// 自定义每页数量更新
mixpus.hook_per_page_select = function () {
	$('.pages-box.link .per-page').change(function (e) {
		e.preventDefault();
		var url = $(this).find('option:selected').data('href');
		window.location.href = url;
    });
};

mixpus.hook_all_check = function() {
	// 全选 or 反选
	$('input.check-all').bind('click', function() {
		if ($(this).is(':checked')){
			$(this)
				.parents('table')
				.find('.check-one')
				.prop('checked', true);
		} else {
			$(this)
				.parents('table')
				.find('.check-one')
				.prop('checked', false);
		}
		mixpus.checked_items_status();
	});

	$('input.check-one').click(function () {
		// 取消全选
		if (!$(this).is(':checked')) {
			$('input.check-all')
				.prop('checked', false);
		}
		mixpus.checked_items_status();
	});
};

mixpus.checked_items_status = function () {
	var total_count = 0;
	$('input.check-one').each(function () {
		if ($(this).is(':checked')) {
			total_count += 1;
		}
	});

	if (total_count > 0) {
		$('.checked-items-status').html(total_count + ' ' + mixpus.locale.selected_label).removeClass('hidden');
		$('.btn.delete-all').removeClass('hidden');
	} else {
		$('.checked-items-status').addClass('hidden');
		$('.btn.delete-all').addClass('hidden');
	}
};

mixpus.hook_delete_all = function () {
	// 删除 全部 or 单个
	$('button.delete-all').click(function () {
		var form_id = $(this).data('form-id');

		swal({
			title: "Confirm to delete?",
			text: "You will not be able to recover!",
			type: "warning",
			showCancelButton: true,
			confirmButtonText: "Yes, delete it!",
			confirmButtonColor: '#008749',
			closeOnConfirm: true
		}).then(function () {
		    // 检测是否选中
            if ($('#' + form_id).find(':checked').length){
                $('#' + form_id).submit();
            } else {
                swal(
                    '出错了',
                    "First to selected the one!!!",
                    'error'
                );
            }
        });
	});
};

mixpus.hook_ajax_modal = function() {
	// 自动绑定ajax的链接
	$('a.ajax-modal').click(function () {
		var url = $(this).attr('href'), modal_name = $(this).data('modal');
		$.get(url, function (html) {
			$('#'+ modal_name).remove();

			$('body').append('<div id="'+ modal_name +'" role="dialog" class="modal">' + html + '</div>');

			$('#'+ modal_name).modal({
				backdrop: false,
				show: true
			});
		});
		return false;
	});
};

// 跟踪订单数量变化
mixpus.tracker_order_change = function () {
	$('#choose-products input.input-quantity')
			.unbind('change')
			.on('change', function () {
				mixpus.order_recount();
			});

    $('a.ajax-remove-item').click(function (e) {
        $('#tr_stock_' + $(this).data('id')).remove();

        mixpus.order_recount();

        return false;
    });
};

// 订单产品数量变化，重新计算数值
mixpus.order_recount = function () {
	var total_quantity=0, total_amount=0, total_discount=0;
	$('#choose-products input.quantity').each(function () {
		var quantity = parseInt($(this).val()), sku_id = $(this).data('id');
		var price = parseFloat($('#sale_price_' + sku_id).html());
		var discount = parseFloat($('#discount_' + sku_id).val());

		$('#deal_price_' + sku_id).html((price - discount).toFixed(2));

		subtotal = price*quantity;
		total_quantity += quantity;
		total_discount += discount;
		total_amount += subtotal;

		$('#subtotal_' + sku_id).html((subtotal - discount).toFixed(2));
	});

	$('#total_quantity').html(total_quantity);
	$('#total_amount').html(total_amount.toFixed(2));
	$('#total_discount').html(total_discount.toFixed(2));
	$('#payable_amount').html((total_amount - total_discount).toFixed(2));
};

// 更新各个状态订单数量
mixpus.update_order_status_count = function (status_count) {
	for (var key in status_count) {
		if (status_count[key] && status_count[key] > 0) {
			$('#' + key).text(status_count[key]).show();
		} else {
			$('#' + key).text(0).hide();
		}
	}
};


mixpus.hook_summer_editor = function () {
	// Override summernotes image manager
	$('.summernote').each(function() {
		var element = this;

		$(element).summernote({
			disableDragAndDrop: true,
			height: 300,
			emptyPara: '',
			toolbar: [
				['font', ['bold', 'underline', 'clear']],
				['para', ['ul', 'ol']],
				['insert', ['link', 'image', 'video']],
				['view', ['fullscreen', 'codeview', 'help']],
				['history', ['undo', 'redo']]
			],
			buttons: {
    			image: function() {
					var ui = $.summernote.ui;

					// create button
					var button = ui.button({
						contents: '<i class="note-icon-picture" />',
						tooltip: $.summernote.lang[$.summernote.options.lang].image.image,
						click: function () {
							$('#modal-image').remove();

							if ($.cookie('img_last_open_folder') && ($.cookie('img_last_open_folder') != 'undefined')) {
								img_last_open_folder = $.cookie('img_last_open_folder');
							}

							$.ajax({
								url: mixpus.urls.show_assets + '?directory=' + mixpus.img_last_open_folder,
								dataType: 'html',
								beforeSend: function() {
									$('#button-image i').replaceWith('<i class="fa fa-circle-o-notch fa-spin"></i>');
									$('#button-image').prop('disabled', true);
								},
								complete: function() {
									$('#button-image i').replaceWith('<i class="fa fa-upload"></i>');
									$('#button-image').prop('disabled', false);
								},
								success: function(html) {
									$('body').append('<div id="modal-image" class="modal">' + html + '</div>');

									$('#modal-image').modal('show');

									$('#modal-image').delegate('a.thumbnail', 'click', function(e) {
										e.preventDefault();

										$(element).summernote('insertImage', $(this).find('img').attr('src'));

										$('#modal-image').modal('hide');
									});
								}
							});
						}
					});

					return button.render();
				}
  			}
		});
	});
};

// 文件上传管理器
mixpus.upload_file_manager = function () {
	// Image Manager
	$(document).on('click', 'a[data-toggle=\'image\']', function(e) {
		var $element = $(this);
		var $popover = $element.data('bs.popover'); // element has bs popover?
		var $target = $(this).data('target');
		var $placement = $(this).data('placement') || 'right';

		e.preventDefault();

		// destroy all image popovers
		$('a[data-toggle="image"]').popover('destroy');

		// remove flickering (do not re-add popover when clicking for removal)
		if ($popover) {
			return;
		}
		
		var ppv = '<button type="button" id="button-image" class="btn btn-mixpus m-r-10"><i class="fa fa-edit"></i></button> <button type="button" id="button-clear" class="btn btn-danger"><i class="fa fa-trash"></i></button>'
		
		if ($target == 'multi-mode') {
			ppv = '<button type="button" id="button-image" class="btn btn-mixpus"><i class="fa fa-edit"></i></button>'
		}
		
		$element.popover({
			html: true,
			placement: $placement,
			trigger: 'manual',
			content: function() {
				return ppv;
			}
		});

		$element.popover('show');

		$('#button-image').on('click', function() {
			var $button = $(this);
			var $icon   = $button.find('> i');

			$('#modal-image').remove();

			if ($.cookie('img_last_open_folder') && ($.cookie('img_last_open_folder') != 'undefined')) {
				mixpus.img_last_open_folder = $.cookie('img_last_open_folder');
			}

			$.ajax({
				url: mixpus.urls.show_assets + '?directory=' + mixpus.img_last_open_folder + '&up_target=' + $target,
				dataType: 'html',
				beforeSend: function() {
					$button.prop('disabled', true);
					if ($icon.length) {
						$icon.attr('class', 'fa fa-circle-o-notch fa-spin');
					}
				},
				complete: function() {
					$button.prop('disabled', false);
					if ($icon.length) {
						$icon.attr('class', 'fa fa-pencil');
					}
				},
				success: function(html) {
					$('body').append('<div id="modal-image" class="modal">' + html + '</div>');

					$('#modal-image').modal('show');
				}
			});

			$element.popover('destroy');
		});

		$('#button-clear').on('click', function() {
			$element.find('img').attr('src', $element.find('img').attr('data-placeholder'));

			$element.parent().find('input').val('');

			$element.popover('destroy');
		});
	});
};