html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width" />
    
    <meta name="ResourceType" content="Forum" />
    <meta name="hgurl" content="invisible" />
    <meta name="threadAnswered" content="true" />
        <meta name="threadTag" content="762" />
    <meta name="lastModified" content="2015-07-21" />
    <meta name="description" content="I have such a code for the grid I&#x27;m using &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;lt;telerik:GridViewDataColumn&amp;nbsp;Header=&quot;Type&quot;&amp;nbsp;DataMemberBi..." />
    <link rel="canonical" href="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems" />

    


    <link rel="shortcut icon" href="/forums/favicon.ico?v=e5kLIm-z6JcLdQ3skdToubWbK3sGnQJD179w_r6O3lM" />



    
    <title>Virtual mode &#x2B; custom cell DataTemplate = problems | Telerik Forums</title>

    <link rel="preconnect" href="https://stats.g.doubleclick.net" />
    <link rel="preconnect" href="https://www.googletagmanager.com" />

    

    <link rel="stylesheet" href="/forums/bundles/forums.min.css?v=3WvqOrQBsNidtvVWEs1GRUbiTdLS_i1dQvZJH_GfNvo" />

    <script async src="/forums/bundles/forums.min.js?v=s3DdvBtu1CS4_0Uj4zC8zwko2wp4rMPT8ejDIy6c0RI"></script>

    <!-- Google Tag Manager -->
    
<script>
    window.isMobile = function () {
        var result = false;
        var matches = [
            /(Windows Phone(?: OS)?)\s(\d+)\.(\d+(\.\d+)?)/,
            /(Silk)\/(\d+)\.(\d+(\.\d+)?)/,
            /(Android|Android.*(?:Opera|Firefox).*?\/)\s*(\d+)\.?(\d+(\.\d+)?)?/,
            /(iPhone|iPod).*OS\s+(\d+)[\._]([\d\._]+)/,
            /(iPad).*OS\s+(\d+)[\._]([\d_]+)/,
            /(MeeGo).+NokiaBrowser\/(\d+)\.([\d\._]+)/,
            /(webOS)\/(\d+)\.(\d+(\.\d+)?)/,
            /(BlackBerry|BB10).*?Version\/(\d+)\.(\d+(\.\d+)?)/,
            /(PlayBook).*?Tablet\s*OS\s*(\d+)\.(\d+(\.\d+)?)/,
            /(MSIE)\s+(\d+)\.(\d+(\.\d+)?)/,
            /(tizen).*?Version\/(\d+)\.(\d+(\.\d+)?)/i,
            /(sailfish).*rv:(\d+)\.(\d+(\.\d+)?).*firefox/i,
            /(Mobile).*rv:(\d+)\.(\d+(\.\d+)?).*Firefox/
        ];
        for (var i = 0; i < matches.length; i++) {
            result = matches[i].test(window.navigator.userAgent);
            if (result) {
                break;
            }
        }
        return result;
    }
</script>

<script type="text/plain" class="optanon-category-2">
        if(isMobile()) {
            window._gaq = window._gaq || [];
            window._gaq.push(['_setAccount', "UA-111455-1"],
            ['_setDomainName', '.telerik.com'],
            ['_addIgnoredRef', 'telerik.com'],
            ['_trackPageview']);

            var ga = document.createElement('script');
            ga.type = 'text/javascript';
            ga.async = true;
            ga.src = '//stats.g.doubleclick.net/dc.js';
            var s = document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(ga, s);
        }
</script>

<script type="text/plain" class="optanon-category-1">
        if(!isMobile()) {
            (function (w, d, s, l, i) {
                w[l] = w[l] || [];
                w[l].push({
                    'gtm.start': new Date().getTime(),
                    event: 'gtm.js'
            });
            var f = d.getElementsByTagName(s)[0],
            j = d.createElement(s),
            dl = l != 'dataLayer' ? '&l=' + l : '';
            j.async = true;
            j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
            f.parentNode.insertBefore(j, f);
            })(window, document, 'script', 'dataLayer', "GTM-6X92");
        }
</script>

<script src="https://cdn.cookielaw.org/consent/3dfce4f2-dab6-4128-9f33-df7e0597da82/otSDKStub.js" data-language="en" type="text/javascript" charset="UTF-8" data-domain-script="3dfce4f2-dab6-4128-9f33-df7e0597da82" async></script></th:partial>
    <!-- End Google Tag Manager -->

    <script>window.$fq = window.$fq || [];</script>
    
    
    
    <script type="text/javascript">
		(function () {
			var userAuthenticated = false;

            window.toggleSort = function () {
                $("#answers").toggleClass("disabled");
            }

			function fetchDataUrl(url) {
				return new Promise((resolve, reject) => {
					fetch(url)
						.then(r => {
							if (r.ok) {
								return r.blob();
							}

							return Promise.reject(`Image request failed with ${r.status}`);
						})
						.then(b => {
							var reader = new FileReader();
							reader.onload = e => resolve(e.target.result);
							reader.readAsDataURL(b);
						})
						.catch(reason => reject(reason));
				});
			}

			function embedImages(html) {
				const $wrapper =  $("<div></div>").html(html);

				const promises = [];

				$wrapper
					.find('img')
					.each((ix, img) => {
						const src = img.getAttribute("src");

						$(img).css("cursor", "").removeAttr("loading");
						
						if (!src || src.indexOf('//') === 0 || src.indexOf("://") > 0) {
							return;
						}

						var p = fetchDataUrl(src).then(dataUrl => img.src = dataUrl).catch(() => img.remove());

						promises.push(p);
					});

				const result = Promise.all(promises).then(() => $wrapper.html());

				return result;
			}

            function initializeSocialShare() {
				var $socialShareBox = $("#social-care-box")
                    , $copyBtn = $("#social-care-box .copyBtn");

                $socialShareBox.find("ul.social-network-list a").on("click", function (e) {
                    e.preventDefault();
                    window.open(this.href, 'newwindow', 'width=550,height=500');
                });

				if (navigator.permissions) {
					navigator.permissions.query({ name: "clipboard-write" })
						.then(function (result) {
							if (result.state == "granted" || result.state == "prompt") {
								$copyBtn.on('click', function () {
									navigator.clipboard.writeText($("#social-care-box .url").val());
									notificationService.success('Link copied to clipboard.');
								});
							} else {
								$copyBtn.hide();
							}
						})
						.catch(function () {
							$copyBtn.on('click', function () {
								$("#social-care-box .url").prop('disabled', false).select().prop('disabled', true);
								document.execCommand('copy');
								notificationService.success('Link copied to clipboard.');
							});
						});
				}

                $socialShareBox.on("click", function (e) { e.stopPropagation(); });
                $("body").on('click', function () {
                    if (!$socialShareBox.is(":visible")) {
                        return true;
                    }

                    $socialShareBox.toggle();
                });
            }

            function initializeSocialShareHandlers() {
                $("a.social-care").on("click", toggleSocialShare);
			}

            function initializeVoteHandlers() {
                $('.vote-touch').off('click').click(toggleVote);
                initializeVoteTitles();
            }

            function initializeVoteTitles() {
                $('.vote-touch > .vote.up').parent().prop('title', 'This answer is helpful.');
                $('.vote-touch > .vote.down').parent().prop('title', 'This answer is not helpful.');

                $('.vote-touch > .vote.selected').parent().prop('title', 'Remove your vote for this answer.');
                $('.vote-touch.disabled > .vote.up').parent().prop('title', 'You have voted for this answer. To remove your vote click on the down arrow.');
                $('.vote-touch.disabled > .vote.down').parent().prop('title', 'You have voted for this answer. To remove your vote click on the up arrow.');

                $('.vote-touch.disabled.own').prop('title', 'You can\'t vote for your own answer.');
            }

			function toggleVote() {
				var userAuthenticated = false;
				if (!userAuthenticated) {
					window.location.href = "/login/v2/telerik?returnUrl=https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems";
					return;
                }

				var $voteTouch = $(this)
					, $voteBtn = $voteTouch.children(".vote")
					, isEnalbed = !$voteBtn.parent().hasClass("disabled")
					, id = $voteBtn.data("id")
					, isUpVote = $voteBtn.hasClass("up")
					, isUndoAction = $voteBtn.hasClass("selected")
					, $oppositeVoteBtn = $voteTouch.siblings('.vote-touch').children('.vote')
					, $score = $voteTouch.siblings(".answer-score")
                    , $loaderContainer = $('#msg-content-' + id + ' .loader-container')
					, request = {
						method: "DELETE",
						url: '/forums/api/v1/forums/threads/messages/' + id + '/votes/mine',
						contentType: "application/json",
						success: function () {
							var currentScore = Number($score.text())
								, updateDirection = isUndoAction ? -1 : 1
								, updateValue = (isUpVote ? 1 : -1) * updateDirection;

							$score.text(currentScore + updateValue);

							$voteBtn.toggleClass("selected");
							$oppositeVoteBtn.parent().toggleClass("disabled");
							initializeVoteTitles();
                            $loaderContainer.hide();
						},
						error: function () {
                            $loaderContainer.hide();
							showDefaultNotificationError();
						}
					};

				if (!isEnalbed) {
					return;
				}

				if (!isUndoAction) {
					request.method = "POST";
					request.data = JSON.stringify({ direction: isUpVote ? 1 : -1 });
				}

                $loaderContainer.show();
				$.ajax(request).then(function () {
                    if (!isUndoAction && isUpVote) {
						achievementNotificationService.checkForNewAchievements('/forums/api/v1/profile/mine', true);
                    }
				});
			}

            function toggleSocialShare(e) {
                e.preventDefault();
				e.stopPropagation();

				var isMobile = window.innerWidth < 992;

                var $this = $(this)
                    , $box = $("#social-care-box")
                    , url = $this.data("url")
                    , title = $this.data("title")
                    , $titleLabel = $box.find(".title")
                    , $urlInput = $box.find(".url")
                    , position = $this.offset()
					, top = position.top + $this.outerWidth()
					, left = position.left + $this.outerWidth() / 2 - $box.width() / 2;

				if (window.navigator.share && isMobile) {
					window.navigator.share({
						url: url
					});
					return;
				}

				if (isMobile) {
					return;
				}

                $urlInput.val($this.data("url"));
                $titleLabel.text(title);
                $box.show().css({ top: top, left: left });
                $urlInput.prop("disabled", false).select().prop("disabled", true).focus();

                $("ul.social-network-list a").each(function (index, element) {
                    var $this = $(element)
                        , shareUrl = $this.data("url").replace("{url}", url);

                    $this.attr("href", shareUrl);
                });
            }

			function showAddCommentForm(button) {
				if (!userAuthenticated) {
					window.location.href = "/login/v2/telerik?returnUrl=https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems";
					return;
				}

				toggleMessageButtons(false);

				var $button = $(button);
				var $form = $button.next();

				Promise.all([
					kendoService.initEditor($form.find('textarea')),
					kendoService.initUpload($form.find('.file-input'), $form.find('.file-upload-container'), '#file-template')
				])
					.then(function () {
					var $textArea = $form.find('textarea');
					$textArea.closest("table.k-editor").addClass("sm-editor");
					$textArea.data('kendoEditor').value('');
					clearValidationErrors($form);
					$(button).hide().next().show();
				});
            }

			function hideCommentForm(button) {
				toggleMessageButtons(true);
				$(button).closest("form").hide().prev().show();
				$(button).closest("form").find('textarea').data('kendoEditor').value('');
			}

			function showEditCommentForm(button) {
				toggleMessageButtons(false);
				var $container = $(button).closest('.answer-container')
				var $form = $container.find('form');

				var files = $container.find('.attachment')
					.map(function () {
						var $el = $(this);
						return {
							id: $el.data('attachmentid'),
							name: $el.text().trim(),
							size: $el.data('filesize'),
							extension: $el.data('extension')
						};
					});

				var commentHtml = $container.find('.comment-text').html();

				Promise.all([
					embedImages(commentHtml),
					kendoService.initEditor($form.find('textarea')),
					kendoService.initUpload($form.find('.file-input'), $form.find('.file-upload-container'), '#file-template', files)
				])
				.then(function ([html]) {
					var $textArea = $form.find('textarea');
					$textArea.closest("table.k-editor").addClass("sm-editor");

					$textArea.data('kendoEditor').value(html);

					clearValidationErrors($form);
					$form.show().prev().hide();
				});
			}

			initializeComments = function () {
				$(".btn-comment").off('click').click(function () { showAddCommentForm(this); });
				$(".btn-edit-comment").off('click').click(function () { showEditCommentForm(this); });

				$(".btn-comment-close").off('click').click(function () { hideCommentForm(this); });
			}

			window.commentSubmitted = function (data, status, xhr) {
				if (xhr.status === 202) {
                    notificationService.error('Your comment has been submitted for review.');
				}

				achievementNotificationService.checkForNewAchievements('/forums/api/v1/profile/mine', true);

				toggleMessageButtons(true);
				$('.btn-subscribe').addClass('subscribed');
				initializeComments();
			}

            window.commentEdited = function (data, status, xhr) {
                if (xhr.status === 202) {
                    notificationService.error('Your comment has been submitted for review.');
                }

                toggleMessageButtons(true);
                $('.btn-subscribe').addClass('subscribed');
                initializeComments();
            }

			var tags = null;
			function initMultiSelectIfPresent($container) {
				var multiSelectElement = $container.find('#tag-select')[0];

				if (!multiSelectElement) {
					return Promise.resolve();
				}

				tags = tags || new Promise(function (resolve, reject) {
					$.getJSON('/forums/api/v1/forums/0/tags', function (data) {
						var result = data.map(function (d) { return { text: d.name, value: d.id } });
						resolve(result);
					}, reject)
				});

				return tags.then(function (dataSource) {
					return kendoService.initMultiSelect(dataSource, multiSelectElement);
				})
				.then(function () {
					var tagIds = $(multiSelectElement).data('tagIds');
					$(multiSelectElement).data('kendoMultiSelect').value(tagIds);
				});
			}

			function showEditPostForm(button) {
				var $container = $(button)
					.closest('.edit-post-popup')
					.addClass('open')
					.closest('.answer-container');

				$(button).toggleClass('Btn loader-btn icon');

				var form = $container.find('.post-edit-form')[0];

				var textArea = $(form).find('textarea')[0];
				var fileInput = $(form).find('.file-input')[0];

				var files = $container.find('.attachment')
					.map(function ()
					{
						var $el = $(this);
						return {
							id: $el.data('attachmentid'),
							name: $el.text().trim(),
							size: $el.data('filesize'),
							extension: $el.data('extension')
						};
					});

				const postHtml = $container.find('.msg-content').html();

				Promise.all([
					embedImages(postHtml),
					kendoService.initUpload(fileInput, $(form).find('.file-upload-container'), '#file-template', files),
					kendoService.initEditor(textArea),
					initMultiSelectIfPresent($container)
				])
				.then(function ([html]) {
						clearValidationErrors(form);
						$(textArea).data('kendoEditor').value(html);
						$(form).show().prev().hide();
						$(button).toggleClass('Btn loader-btn icon').closest('.actions-container').hide();
						$(".edit-overlay").show();
				});
			}

			function toggleMessageButtons(enabled) {
				$('.btn-add-answer,.btn-comment,.btn-accept,.btn-edit-post,.btn-edit-comment').prop('disabled', !enabled)
			}

			function showAnswerForm() {
				if (!userAuthenticated) {
					window.location.href = "/login/v2/telerik?returnUrl=https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems";
					return;
				}

				toggleMessageButtons(false);

				$('.btn-add-answer').prop('disabled', true).addClass('Btn loader-btn');

				var form = $('.answer-form')[0];

				Promise.all([
					kendoService.initEditor($('.answer-form textarea')),
					kendoService.initUpload('.answer-form .file-input', '.answer-form .file-upload-container', '#file-template')
				])
					.then(function () {
						clearValidationErrors(form);
						$('.answer-form textarea').data('kendoEditor').value('');
						$('.answer-form .file-input').data('kendoUpload').removeAllFiles();
						$('.btn-add-answer').prop('disabled', false).removeClass('Btn loader-btn').hide();
						$('.answer-form').show();
				});
			}

			function hideAnswerForm(button) {
				toggleMessageButtons(true);
				$(".edit-overlay").hide();
				$(button).closest('.edit-post-popup').removeClass('open');
				$(button).closest('.answer-container').find('.actions-container').show();
				$(button).closest('form').hide().prev().show();
			}

			function initializeAnswers() {
				$('.btn-add-answer').off('click').click(function () { showAnswerForm(); });
				$('.btn-cancel-answer').off('click').click(function () { hideAnswerForm(this); });
				$('.btn-edit-post').off('click').click(function () { showEditPostForm(this); });
				$("#sortDropdown").off('change').change(function () { $(this).parent().parent().submit(); });

			}

			function scrollToHash(hash) {
				var $hash = $(hash);

				if (!$hash.length) {
					return;
				}

				window.scrollTo(0, $hash.offset().top - $navHeight - 30);
            }

			function initializeLocationHashHandler() {
				window.addEventListener("hashchange", function () {
                    scrollToHash(document.location.hash);
                });

                if (document.location.hash) {
                    $navHeight = $("#js-tlrk-nav").height();
					setTimeout(function () {
                        scrollToHash(document.location.hash);
                    }, 1000);
                }
            }

			window.initializeThreadMessageHandlers = function () {
				initializeAnswers();
				initializeSocialShareHandlers();
				initializeComments();
				initializeVoteHandlers();
			}

            window.postSubmitted = function (data, status, xhr) {
                if (xhr.status === 202) {
                    notificationService.error('Your answer has been submitted for review.');
				}

				achievementNotificationService.checkForNewAchievements('/forums/api/v1/profile/mine', true);

				initializeThreadMessageHandlers();
			}

            window.postEdited = function (data, status, xhr) {
                if (xhr.status === 202) {
                    notificationService.error('Your answer has been submitted for review.');
                }

                initializeThreadMessageHandlers();
            }

            $fq.push(function () {

				initializeSocialShare();
				initializeThreadMessageHandlers();
                initializeLocationHashHandler();

                $.get('/forums/api/v1/forums/threads/270345/viewscounter');
            });
        })();
    </script>

    <div id="code-format-window"></div>
    <script id="code-format-template" type="text/x-custom-template">
		<div class="code-format-container">
    <p class="code-format-title u-mt0">Insert Code</p>
    <div class="u-mt20">
        <label for="paste-code" class="d-inline-block u-mb10">Type or paste code:</label>
        <textarea id="paste-code"></textarea>
    </div>

    <div class="u-mt20">
        <label for="lang" class="u-dib">Preview language:</label>
        <div class="dropdown u-ml10 u-mr10">
            <select id="lang-dropdown"></select>
        </div>
        <button id="code-preview" onClick="kendoEditorService.onPreview(event)" class="btn-outline">Preview</button>
    </div>

    <div id="preview" class="u-mt20"></div>

    <div class="d-flex u-mt20">
        <button type="button" onClick="kendoEditorService.onInsert(event)" class="btn-accent-sm">Insert code</button>
        <a href="#" onClick="kendoEditorService.onClose(event)" class="btn-cancel-sm u-ml20">Cancel</a>
    </div>
</div>
    </script>

    <script id="file-template" type="text/x-kendo-template">
		<div class="file-wrapper">
    <span class="k-progress"></span>
    <span class="file-upload-text">#=name#</span>
    <span class="file-upload-text-muted"> - #: kendoUploadService.getFormattedFilesSize(size) #</span>
    <strong class="k-upload-status">
        <button type="button" class="k-button k-upload-action" aria-label="Remove"></button>
        <button type="button" class="k-button k-upload-action" aria-label="Retry"></button>
    </strong>
</div>
    </script>

</head>
<body class="d-flex flex-column">
    <!-- Google Tag Manager (noscript) -->
    <noscript>
        <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-6X92"
                height="0" width="0" style="display:none;visibility:hidden"></iframe>
    </noscript>
    <!-- End Google Tag Manager (noscript) -->

    
<link rel="preload" href="https://d6vtbcy3ong79.cloudfront.net/fonts/2.2.7/css/metric.min.css" as="style" media="(min-width: 621px)"><link rel="preload" href="https://d6vtbcy3ong79.cloudfront.net/fonts/2.2.7/metric/Metric-Light.woff2" as="font" crossorigin="anonymous" media="(min-width: 621px)"><link rel="preload" href="https://d6vtbcy3ong79.cloudfront.net/fonts/2.2.7/metric/Metric-Medium.woff2" as="font" crossorigin="anonymous" media="(min-width: 621px)"><link rel="preload" href="https://d6vtbcy3ong79.cloudfront.net/fonts/2.2.7/metric/Metric-Regular.woff2" as="font" crossorigin="anonymous" media="(min-width: 621px)"><link rel="preload" href="https://d6vtbcy3ong79.cloudfront.net/fonts/2.2.7/metric/Metric-Semibold.woff2" as="font" crossorigin="anonymous" media="(min-width: 621px)"><link rel="preload" href="https://d6vtbcy3ong79.cloudfront.net/telerik-navigation/3.5.52/css/index.min.css" as="style"><style id="js-tlrk-nav-inline-styles">.TK-Nav--Loading,.TK-Nav--Loading *{box-sizing:border-box}.TK-Nav--Loading{overflow:hidden;background:#fff;font-family:Metric}.TK-Nav--Loading>.TK-Bar{overflow:hidden;background:#fff}.TK-Nav--Loading .TK-container{max-width:1230px;margin:0 auto;padding:0 30px}.TK-Nav--Loading .TK-TLRK-Brand{margin:0}.TK-Nav--Loading .TK-Dropdown,.TK-Nav--Loading .TK-Nav-Overlay,.TK-Nav--Loading .TK-Print{display:none}.TK-Nav--Loading .TK-Context-Menu,.TK-Nav--Loading .TK-Products-Menu-Item-Button{visibility:hidden}@media only screen and (min-width:1240px){.TK-Nav--Loading,.TK-Nav--Loading>.TK-Bar{height:60px}}@media only screen and (max-width:1239px){.TK-Nav--Loading,.TK-Nav--Loading>.TK-Bar{height:45px}}@media only screen and (max-width:1229px){.TK-Nav--Loading .TK-container{padding:0 20px}}</style><link rel="stylesheet" type="text/css" href="https://d6vtbcy3ong79.cloudfront.net/fonts/2.2.7/css/metric.min.css" id="js-tlrk-nav-metric" class="is-loading" onload="this.classList.remove('is-loading')" onerror="this.classList.remove('is-loading')"><link rel="stylesheet" type="text/css" href="https://d6vtbcy3ong79.cloudfront.net/telerik-navigation/3.5.52/css/index.min.css" id="js-tlrk-nav-styles" class="is-loading" onload="this.classList.remove('is-loading')" onerror="this.classList.remove('is-loading')"><nav id="js-tlrk-nav" class="TK-Nav TK-Nav--Shadow TK-Nav--Loading" data-tlrk-nav-version="3.5.52" data-tlrk-nav-template="nav-main-noa-rel-component"><section class="TK-Bar"><div class="TK-container TK-Bar-container"><figure class="TK-TLRK-Brand TK-TLRK-Brand--Full"><a href="#skip-to-content" id="js-tlrk-skip-link" class="TK-Skip-Link">skip navigation</a> <a href="/" class="TK-TLRK-Logo" aria-label="Go to Homepage"><svg xmlns="http://www.w3.org/2000/svg" width="147" height="60" viewBox="0 0 400.4 60.3"><path fill="#7c878e" d="M396.7 18.4c-2 0-3.7 1.6-3.7 3.7 0 2.2 1.7 3.7 3.7 3.7s3.7-1.6 3.7-3.7c0-2.2-1.7-3.7-3.7-3.7zm0 6.8c-1.7 0-3-1.3-3-3.1s1.3-3.1 3-3.1 3 1.3 3 3.1-1.3 3.1-3 3.1z"/><path fill="#7c878e" d="M398.5 21.5c0-.9-.6-1.4-1.4-1.4h-1.8V24h1.1v-1.2h.3l.8 1.2h1.2l-.9-1.4c.4-.1.7-.5.7-1.1zm-1.6.4h-.6V21h.6c.3 0 .5.2.5.4 0 .4-.2.5-.5.5zm-103.5-7.7h-28.5v2.6h12.7v32.4h2.9V16.8h12.9zm7.4 9.1c-6.7 0-10.9 5.6-10.9 13.4 0 7.9 4.7 12.9 11.8 12.9 3 0 5.5-.7 7.4-2.2v-2.7c-2.2 1.8-4.3 2.5-7.1 2.5-5.2 0-9.2-3.6-9.2-10.4H311v-1c-.2-7.4-3.6-12.5-10.2-12.5zm-8 11.1c.7-5.5 3.9-8.6 8-8.6 5 0 7.1 4.1 7.3 8.6h-15.3zM315 12.1h2.9v37.1H315zm18.1 11.2c-6.7 0-10.9 5.6-10.9 13.4 0 7.9 4.7 12.9 11.8 12.9 3 0 5.5-.7 7.4-2.2v-2.7c-2.2 1.8-4.3 2.5-7.1 2.5-5.2 0-9.2-3.6-9.2-10.4h18.2v-1c-.1-7.4-3.6-12.5-10.2-12.5zm-8 11.1c.7-5.5 3.9-8.6 8-8.6 5 0 7.1 4.1 7.3 8.6h-15.3zm25-6.5v-4h-2.9v25.3h2.9V31.5c1.2-3.2 3.6-5.5 6.7-5.5.9 0 1.7.2 2.3.5v-2.8c-.6-.2-1.3-.3-2.2-.3-3.1-.1-5.7 2-6.8 4.5zm12.1-4h2.8v25.3h-2.8zm1.5-9.7c-1.1 0-1.9.9-1.9 1.9 0 1.1.9 1.9 1.9 1.9s1.9-.9 1.9-1.9-.8-1.9-1.9-1.9zm26.5 9.7h-3.7l-12.8 11V12.1h-2.9v37.1h2.9v-13l13.2 13h3.5l-13.8-13.8z"/><path fill="#5ce500" d="M11.2 14.9L0 21.3l17.4 10.1v20.1l11.2-6.4c.5-.3.9-1 .9-1.6V24.4L13 14.9c-.5-.3-1.3-.3-1.8 0z"/><path fill="#5ce500" d="M12.1 48.4V34.5L0 41.5zM25 .2c-.5-.3-1.3-.3-1.8 0L10.7 7.4l24.1 13.9v27.9L47.3 42c.5-.3.9-1 .9-1.6V13.6L25 .2z"/><path fill="#4b4e52" d="M117.9 22.5c-4.3 0-7.7 1.6-9.8 4.7-2.3 3.2-2.6 7-2.6 9 0 8.3 4.9 13.6 12.5 13.6 9.2 0 12.5-7.4 12.5-13.8 0-3.7-1.1-7-3.1-9.4-2.3-2.7-5.6-4.1-9.5-4.1zm0 22.4c-4.2 0-6.9-3.4-6.9-8.8 0-5.5 2.6-8.9 6.9-8.9 4.2 0 6.9 3.4 6.9 8.8 0 5.5-2.7 8.9-6.9 8.9zM74.8 13.6H61.7v35.6h5.8v-14h7.4c8 0 12.4-3.9 12.4-11-.1-3.1-1.3-10.6-12.5-10.6zM74.1 30h-6.6V18.9h7.4c4.3 0 6.4 1.8 6.4 5.5 0 4-2.1 5.6-7.2 5.6zm26.6-7.3c-2.2.3-3.9 1.4-5.2 3.5V23h-5.1v26.1h5.4V37.9c0-5.2.4-9.6 5.9-9.6.6 0 1.1.1 1.7.3l.7.2 1-5.3-.4-.2c-1.2-.5-2.6-.7-4-.6zm145 12.1c-1.3-.5-4-1.2-6.1-1.7-1-.3-1.9-.5-2.5-.7-2-.6-3-1.4-3-2.6 0-2.5 3.5-2.8 5-2.8 1.8 0 4.8.5 5.3 3.5l.1.4h5.2v-.5c-.4-5.3-4-7.8-10.8-7.8-5.1 0-10.2 2.4-10.2 7.6 0 2.8 1.9 5.2 5.2 6.3 1.3.5 3.5 1.1 5.6 1.7 1.2.3 2.4.7 3.3.9 1.6.5 2.4 1.4 2.4 2.6 0 2.4-2.9 3.3-5.6 3.3-2.5 0-5.5-.7-6.2-3.9l-.1-.4h-5.2l.1.6c.5 5.4 4.6 8.3 11.4 8.3 7.7 0 11.2-4.2 11.2-8.4-.1-3-1.8-5.2-5.1-6.4zm-94-9.6c-1.7-1.8-4.1-2.7-7-2.7-7.9 0-11.5 7-11.5 13.5 0 6.6 3.6 13.4 11.5 13.4 2.7 0 5-1 6.7-2.7 0 1.2 0 2.3-.1 2.7-.3 4.3-2.4 6.3-6.5 6.3-2.3 0-4.9-.8-5.4-3.1l-.1-.5H134l.1.7c.6 4.6 4.6 7.5 10.6 7.5 5.2 0 8.9-2 10.8-5.7.9-1.8 1.3-4.4 1.3-7.8V23.1h-5.1v2.1zm-6.6 19.3c-1.9 0-6.3-.9-6.3-8.8 0-5.2 2.5-8.4 6.4-8.4 3.1 0 6.3 2.2 6.3 8.4.1 5.5-2.3 8.8-6.4 8.8zm75.6-9.7c-1.3-.5-4-1.2-6.1-1.7-1-.3-1.9-.5-2.5-.7-2-.6-3-1.4-3-2.6 0-2.5 3.5-2.8 5-2.8 1.8 0 4.8.5 5.3 3.5l.1.4h5.2v-.5c-.4-5.3-4-7.8-10.8-7.8-5.1 0-10.2 2.4-10.2 7.6 0 2.8 1.9 5.2 5.2 6.3 1.3.5 3.5 1.1 5.6 1.7 1.2.3 2.4.7 3.3.9 1.6.5 2.4 1.4 2.4 2.6 0 2.4-2.9 3.3-5.6 3.3-2.5 0-5.5-.7-6.2-3.9l-.1-.4h-5.2l.1.6c.5 5.4 4.6 8.3 11.4 8.3 7.7 0 11.2-4.2 11.2-8.4 0-3-1.7-5.2-5.1-6.4zm-19.9 0c-.3-7.3-5-12.2-11.9-12.2-4 0-7.3 1.6-9.5 4.5-1.8 2.4-2.8 5.7-2.8 9.1 0 8.1 5 13.5 12.5 13.5 5.8 0 9.8-2.9 11.2-8.3l.2-.6h-5.4l-.1.3c-1.1 3.2-3.8 3.9-5.9 3.9-4.1 0-6.7-2.7-7-7.1h18.5l.1-.5c.1-.6.1-1.5.1-2.1v-.5zm-18.4-1.6c.5-3.6 2.9-5.9 6.5-5.9 2.7 0 5.9 1.6 6.3 5.9h-12.8zm-10.5-10.5c-2.2.3-3.9 1.4-5.2 3.5V23h-5.1v26.1h5.4V37.9c0-5.2.4-9.6 5.9-9.6.6 0 1.1.1 1.7.3l.7.2 1-5.3-.4-.2c-1.2-.5-2.6-.7-4-.6zm84.8-1.2c0-.9-.6-1.4-1.4-1.4h-1.8V24h1.1v-1.2h.3l.8 1.2h1.2l-.9-1.4c.4-.1.7-.5.7-1.1zm-1.5.4h-.6V21h.6c.3 0 .5.2.5.4 0 .4-.2.5-.5.5z"/><path fill="#4b4e52" d="M255 18.4c-2 0-3.7 1.6-3.7 3.7 0 2.2 1.7 3.7 3.7 3.7s3.7-1.6 3.7-3.7c0-2.2-1.7-3.7-3.7-3.7zm0 6.8c-1.7 0-3-1.3-3-3.1s1.3-3.1 3-3.1 3 1.3 3 3.1-1.4 3.1-3 3.1z"/></svg></a></figure><ul class="TK-Products-Menu"><li class="TK-Products-Menu-Item TK-Static"><button type="button" class="TK-Products-Menu-Item-Button" aria-label="Product Navigation">All Products <i class="TK-Arrow"></i></button><div id="js-tlrk-nav-dash" class="TK-Dash TK-Dropdown TK-Dropdown--Full TK-Dropdown--White TK-Dropdown---Mobile"><div class="TK-container"><div class="TK-row"><div class="TK-col-6"><div class="TK-Bundles TK-BG"><p class="TK-Dash-Title">Product Bundles</p><a href="/devcraft" class="TK-Bundle" data-match-exact-path><div class="TK-Bundle-Icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 70" width="75" height="61"><path d="M70 35c0 5.3-1.2 10.3-3.2 14.7-4.8 10.4-14.6 18-26.4 19.8-1.8.4-3.6.5-5.4.5-2.6 0-5.1-.3-7.5-.8-6.9-1.5-13.1-5.1-17.8-10C7.1 56.5 5 53.4 3.4 50c-.4-.8-.7-1.5-1-2.3C.8 43.7 0 39.5 0 35 0 15.7 15.7 0 35 0s35 15.7 35 35z" fill-rule="evenodd" clip-rule="evenodd" fill="#a3d8f1"/><path d="M40.9 65.6l-.5 4c-1.8.3-3.6.4-5.4.4-2.6 0-5.1-.3-7.5-.8-6.9-1.5-13.1-5.1-17.8-10C7.1 56.5 5 53.4 3.4 50c3.2-4.4 8.2-7.5 14-8.3 1-.1 1.9-.2 2.9-.2.6 0 1.1 0 1.7.1 4.7.4 8.9 2.3 12.2 5.2 3 2.7 5.3 6.2 6.3 10.1.7 2.7.9 5.7.4 8.7z" fill-rule="evenodd" clip-rule="evenodd" fill="#e26841"/><path d="M17.3 48.5L32 61.3l13.2-7-10-8c-1.4-1.1-2.3-2.9-2.3-4.7v-9H17.3v15.9z" fill="#31475c" fill-rule="evenodd" clip-rule="evenodd"/><path d="M21.9 32.6v15.9l-2.3 2-9.9 8.7C7.1 56.5 5 53.4 3.4 50c-.4-.8-.7-1.5-1-2.3L4 46.3c1.4-1.1 2.3-2.9 2.3-4.7v-9h15.6z" fill="#31475c" fill-rule="evenodd" clip-rule="evenodd"/><defs><filter id="tlrk-nav-a" filterUnits="userSpaceOnUse" x="28.1" y=".3" width="31.2" height="17.4"><feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"/></filter></defs><mask maskUnits="userSpaceOnUse" x="28.1" y=".3" width="31.2" height="17.4" id="tlrk-nav-b"><g filter="url(#tlrk-nav-a)"><path d="M25.7 10.8l32.5-11L61.4 9 28.8 20z" fill="#fff" fill-rule="evenodd" clip-rule="evenodd"/></g></mask><path d="M28.1 17.8l9.1-8.4c2-1.9 4.9-2.3 7.4-1 3 1.5 6.6.5 8.4-2.3L56.6.4 59.3 3l-5.1 7.2c-1.9 2.7-5.6 3.5-8.5 1.9l-1.1-.6c-2.1-1.2-4.6-1.1-6.7.2l-9.8 6.1z" mask="url(#tlrk-nav-b)" fill-rule="evenodd" clip-rule="evenodd" fill="#e26841"/><path d="M62.8 13.7l-8 6.2a6.61 6.61 0 01-8.2 0l-3.2-2.5c-1.4-1.1-3.2-1.6-5-1.3l-10.2 1.5 10.1-3.7c1.9-.7 4.1-.5 5.8.6l2.5 1.6c2.5 1.5 5.7 1.3 7.9-.6l5.6-4.8 2.7 3z" fill-rule="evenodd" clip-rule="evenodd" fill="#e26841"/><path d="M27 11.6h-5.5c-8.4 0-15.3 6.8-15.3 15.3v15.6c0 3.4 2.7 6.1 6.1 6.1H27c3.4 0 6.1-2.7 6.1-6.1V17.7c0-3.4-2.8-6.1-6.1-6.1" fill-rule="evenodd" clip-rule="evenodd" fill="#14254c"/><path d="M31.7 32.2c0 6.7-5.4 12.1-12.1 12.1S7.5 38.8 7.5 32.2s5.4-12.1 12.1-12.1 12.1 5.4 12.1 12.1" fill="#31475c" fill-rule="evenodd" clip-rule="evenodd"/><defs><filter id="tlrk-nav-c" filterUnits="userSpaceOnUse" x="9.1" y="15.8" width="21.1" height="34"><feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"/></filter></defs><mask maskUnits="userSpaceOnUse" x="9.1" y="15.8" width="21.1" height="34" id="tlrk-nav-d"><g filter="url(#tlrk-nav-c)"><path d="M7.5 32.2c0 6.7 5.4 12.1 12.1 12.1 6.7 0 12.1-5.4 12.1-12.1 0-6.7-5.4-12.1-12.1-12.1-6.7 0-12.1 5.4-12.1 12.1z" fill="#fff" fill-rule="evenodd" clip-rule="evenodd"/></g></mask><path d="M9.1 48.1V26.3c0-5.8 4.7-10.5 10.5-10.5s10.5 4.7 10.5 10.5v23.5l-21-1.7z" mask="url(#tlrk-nav-d)" fill-rule="evenodd" clip-rule="evenodd" fill="#e9ac6a"/><path d="M14.6 35.1h5.5v-9.5z" fill="#dc7f1b" fill-rule="evenodd" clip-rule="evenodd"/><path d="M20.3 39.3c1.3.1 2.7-.2 4-1 1.1-.6 1.8-1.5 2.3-2.3l-1-.6c-.4.7-1.1 1.4-1.9 1.9-1.1.7-2.3.9-3.3.8l-.1 1.2z" fill="#fff"/><path d="M27.4 27.6h-2.3c0-.6.5-1.1 1.1-1.1h.2c.5 0 1 .5 1 1.1m-13.5 0h-2.3c0-.6.5-1.1 1.1-1.1h.2c.6 0 1 .5 1 1.1" fill="#231f20" fill-rule="evenodd" clip-rule="evenodd"/><path d="M7.5 24.7h25.1v-1.2H7.5zm0 5.5h25.1V29H7.5zm0 11h23.6v-1.3H7.5zm0-5.5h25.1v-1.3H7.5z" fill="#14254c"/><path d="M66.8 49.7c-4.8 10.4-14.6 18-26.4 19.8-1.8.4-3.6.5-5.4.5-2.6 0-5.1-.3-7.5-.8l-.4-2.8c-.5-3.1-.3-6.2.4-9 1.1-4.2 3.4-7.9 6.5-10.7.2-.2.5-.5.8-.7 3.8-3.2 8.7-5.1 14.2-5.1 7.3 0 13.7 3.5 17.8 8.8z" fill-rule="evenodd" clip-rule="evenodd"/><g fill-rule="evenodd" clip-rule="evenodd"><path d="M56.503 26.65c5.8-3 11.9-4.7 16.4-2.3 2.5 1.4 3.1 3.3 5.4 4 3 .9 7.5-.8 14.8-9.4l4.1 4.4c-10.7 10.6-16.4 11.8-19.7 10.4-2.6-1-3.2-3.4-6.7-5.5-4.8-2.7-10.3-2.4-14.3-1.6" fill="#8174f2"/><path d="M58.003 26.05c2.9-7.4 9.8-11.7 16-10.9 4.9.7 7.9 4.3 8.7 5.5-1.6.9-3.2 1.9-4.8 2.8-1.2-1-3-2.2-5.4-2.8-7.6-1.8-14 4.9-14.5 5.4" fill="#8174f2"/><path d="M37.103 44.85l-2-13.4c0-7.4 6.1-13.4 13.5-13.4s13.5 6 13.5 13.4l-1.7 13.4c-.8 5.8-5.8 10.1-11.6 10.1s-10.8-4.3-11.7-10.1z" fill="#00264b"/><path d="M34.803 34.25h27.5v-5.8h-27.5z" fill="#8174f2"/><path d="M57.003 38.05h-16.5c-1.8 0-3.3-1.5-3.3-3.3 0-1.8 1.5-3.3 3.3-3.3h16.5c1.8 0 3.3 1.5 3.3 3.3 0 1.8-1.5 3.3-3.3 3.3" fill="#e9ac6a"/><path d="M39.203 35.05c0-.6.5-1.1 1.1-1.1.6 0 1.1.5 1.1 1.1m11 .1c0-.6.5-1.1 1.1-1.1s1.1.5 1.1 1.1" fill="#00264b"/><path d="M46.403 38.05h2.9v-5.5z" fill="#dc7f1b"/></g></svg></div><p class="TK-Bundle-Title TK-Best-Value">DevCraft</p><p class="TK-Bundle-Description">All Telerik .NET tools and Kendo UI JavaScript components in one package. Now enhanced with:</p><ul class="TK-Bundle-list"><li><strong>NEW</strong>: Design Kits for Figma</li><li>Online Training</li><li>Document Processing Library</li><li>Embedded Reporting for web and desktop</li></ul></a></div></div><div class="TK-col-18"><div class="TK-row"><div class="TK-col-8"><p class="TK-Dash-Title">Web</p><div class="TK-Dash-Links"><a href="/kendo-ui" class="TK-Dash-Link" data-match-exact-path>Kendo UI</a> <a href="/kendo-jquery-ui" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>UI for jQuery</a> <a href="/kendo-angular-ui" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>UI for Angular</a> <a href="/kendo-react-ui" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>UI for React</a> <a href="/kendo-vue-ui" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>UI for Vue</a> <a href="/blazor-ui" class="TK-Dash-Link" data-match-exact-path>UI for Blazor</a> <a href="/aspnet-core-ui" class="TK-Dash-Link" data-match-exact-path>UI for ASP.NET Core</a> <a href="/aspnet-mvc" class="TK-Dash-Link" data-match-exact-path>UI for ASP.NET MVC</a> <a href="/products/aspnet-ajax.aspx" class="TK-Dash-Link" data-match-exact-path>UI for ASP.NET AJAX</a></div><p class="TK-Dash-Title">Mobile</p><div class="TK-Dash-Links"><a href="/maui-ui" class="TK-Dash-Link" data-match-exact-path>UI for .NET MAUI</a> <a href="/xamarin-ui" class="TK-Dash-Link" data-match-exact-path>UI for Xamarin</a></div><p class="TK-Dash-Title">Document Management</p><div class="TK-Dash-Links"><a href="/document-processing-libraries" class="TK-Dash-Link" data-match-exact-path>Telerik Document Processing</a></div></div><div class="TK-col-8"><p class="TK-Dash-Title">Desktop</p><div class="TK-Dash-Links"><a href="/maui-ui" class="TK-Dash-Link" data-match-exact-path>UI for .NET MAUI</a> <a href="/winui" class="TK-Dash-Link" data-match-exact-path>UI for WinUI</a> <a href="/products/winforms.aspx" class="TK-Dash-Link" data-match-exact-path>UI for WinForms</a> <a href="/products/wpf/overview.aspx" class="TK-Dash-Link" data-match-exact-path>UI for WPF</a></div><p class="TK-Dash-Title">Reporting</p><div class="TK-Dash-Links"><a href="/products/reporting.aspx" class="TK-Dash-Link" data-match-exact-path>Telerik Reporting</a> <a href="/report-server" class="TK-Dash-Link" data-match-exact-path>Telerik Report Server</a></div><p class="TK-Dash-Title">Testing &amp; Mocking</p><div class="TK-Dash-Links"><a href="/teststudio" class="TK-Dash-Link" data-match-exact-path>Test Studio</a> <a href="/teststudio-dev" class="TK-Dash-Link" data-match-exact-path>Test Studio Dev Edition</a> <a href="/products/mocking.aspx" class="TK-Dash-Link" data-match-exact-path>Telerik JustMock</a></div><p class="TK-Dash-Title">CMS</p><div class="TK-Dash-Links"><a href="https://www.progress.com/sitefinity-cms" class="TK-Dash-Link" data-match-exact-path>Sitefinity</a></div></div><div class="TK-col-8"><p class="TK-Dash-Title">UI/UX Tools</p><div class="TK-Dash-Links"><a href="/themebuilder" class="TK-Dash-Link TK-Updated" data-match-exact-path>ThemeBuilder</a> <a href="/design-system" class="TK-Dash-Link" data-match-exact-path>Design System Kit</a> <a href="/page-templates-and-ui-blocks" class="TK-Dash-Link" data-match-exact-path>Templates and Building Blocks</a></div><p class="TK-Dash-Title">Debugging</p><div class="TK-Dash-Links"><a href="/fiddler" class="TK-Dash-Link" data-match-exact-path>Fiddler</a> <a href="/fiddler/fiddler-everywhere" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>Fiddler Everywhere</a> <a href="/fiddler/fiddler-classic" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>Fiddler Classic</a> <a href="/fiddler/fiddlercap" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>FiddlerCap</a> <a href="/fiddlercore" class="TK-Dash-Link TK-Dash-Link--Indented" data-match-exact-path>FiddlerCore</a></div><p class="TK-Dash-Title"></p><div class="TK-Dash-Links"></div><p class="TK-Dash-Title">Free Tools</p><div class="TK-Dash-Links"><a href="https://converter.telerik.com" class="TK-Dash-Link">VB.NET to C# Converter</a> <a href="/teststudio/testing-framework" class="TK-Dash-Link" data-match-exact-path>Testing Framework</a></div></div></div><div class="TK-Dash-Footer"><a href="/all-products" class="TK-Dash-Featured-Link" data-match-exact-path>View all products</a></div></div></div></div></div><div class="TK-Dash-Extension TK--Mobile"></div></li></ul><div class="TK-Drawer" id="js-tlrk-nav-drawer"><ul class="TK-Context-Menu TK-Menu"><li class="TK-Menu-Item"><a href="/support/demos" class="TK-Menu-Item-Link" data-match-exact-path>Demos</a></li><li class="TK-Menu-Item"><a href="/services" class="TK-Menu-Item-Link" data-match-exact-path>Services</a></li><li class="TK-Menu-Item"><a href="/blogs" class="TK-Menu-Item-Link" data-match-starts-with-path>Blogs</a></li><li class="TK-Menu-Item"><a href="/support" class="TK-Menu-Item-Link" data-match-exact-path data-match-pattern data-pattern="telerik.com/support/kb/aspnet-ajax|telerik.com/support/kb/silverlight|telerik.com/support/kb/justmock">Docs &amp; Support</a></li><li class="TK-Menu-Item"><a href="/purchase.aspx" class="TK-Menu-Item-Link" data-match-exact-path>Pricing</a></li></ul><ul class="TK-Aside-Menu TK-Aside-Menu--Max"><li class="TK-Aside-Menu-Item TK-Aside-Menu-Button--Search"><a href="/search" class="TK-Aside-Menu-Link js-tlrk-nav-search-link" title="Search" data-match-exact-path><svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="15" height="15" viewBox="0 0 512 512" xml:space="preserve"><path d="M504.4,464L378.9,338.5c25.6-34.8,40.8-77.7,40.8-124.2c0-115.7-94.1-209.8-209.8-209.8C94.2,4.5,0,98.6,0,214.3 C0,330,94.2,424.1,209.9,424.1c50.5,0,96.9-17.9,133.1-47.8l124.5,124.5c5.1,5.1,11.8,7.6,18.4,7.6s13.3-2.5,18.4-7.6 C514.6,490.7,514.6,474.2,504.4,464z M52.2,214.3c0-87,70.7-157.7,157.7-157.7s157.7,70.7,157.7,157.7c0,41-15.7,78.3-41.4,106.4 c-0.3,0.3-0.7,0.6-1,0.9c-0.7,0.7-1.3,1.4-1.9,2.2c-28.7,29.7-68.9,48.2-113.4,48.2C122.9,372,52.2,301.3,52.2,214.3z"></path></svg></a></li><li class="TK-Aside-Menu-Item"><a href="https://store.progress.com/shopping-cart" data-empty-url="/purchase.aspx?filter&#x3D;web" class="TK-Aside-Menu-Link js-tlrk-nav-shopping-cart-counter-container" aria-label="Shopping cart" title="Shopping cart" data-match-exact-path><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path d="M11.75 14.5a1 1 0 111-1 1 1 0 01-1 1zm-8.25 0a1 1 0 111-1 1 1 0 01-1 1zm8.18-3H4.25A1.752 1.752 0 012.5 9.75v-8a.25.25 0 00-.25-.25H.75a.75.75 0 010-1.5h1.5A1.752 1.752 0 014 1.75v.75h8.78a1.75 1.75 0 011.72 2.093l-1.1 5.5a1.754 1.754 0 01-1.72 1.407zM4 4v5.75a.25.25 0 00.25.25h7.43a.251.251 0 00.245-.2l1.1-5.5a.251.251 0 00-.245-.3z" transform="translate(.75 .75)"/></svg> <span class="TK-Aside-Menu-Link-Text">Shopping cart</span></a></li><li class="TK-Aside-Menu-Item TK--Not-Auth" id="js-tlrk-nav-not-auth-container"><a href="/account/" title="Your Account" class="TK-Aside-Menu-Button" data-match-exact-path><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path xmlns="http://www.w3.org/2000/svg" d="M13.75 14.5a.751.751 0 01-.75-.75v-.5a5.75 5.75 0 10-11.5 0v.5a.75.75 0 01-1.5 0v-.5a7.175 7.175 0 011.319-4.159A7.262 7.262 0 014.69 6.476 3.717 3.717 0 013.5 3.75a3.75 3.75 0 117.5 0 3.716 3.716 0 01-1.19 2.726 7.263 7.263 0 013.371 2.615A7.175 7.175 0 0114.5 13.25v.5a.751.751 0 01-.75.75zm-6.5-13A2.25 2.25 0 109.5 3.75 2.253 2.253 0 007.25 1.5z" transform="translate(.75 .75)"/></svg> <span class="TK-Aside-Menu-Button-Text">Login</span></a></li><li class="TK-Aside-Menu-Item TK-bn"><a href="/contact" class="TK-Aside-Menu-Button TK-Button--CTA-Sec" title="Contact Us" data-match-starts-with-path><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path d="M12.75 14.5h-11A1.752 1.752 0 010 12.753v-7.37a.092.092 0 01.005-.026.1.1 0 000-.023.782.782 0 01.01-.093.63.63 0 01.02-.071l.007-.021V5.14a.828.828 0 01.036-.088.673.673 0 01.045-.078.078.078 0 00.009-.02.069.069 0 01.01-.02.1.1 0 01.028-.019.1.1 0 00.019-.015.68.68 0 01.077-.076.124.124 0 00.015-.024.106.106 0 01.019-.016L6.2.354a1.736 1.736 0 012.1 0l5.9 4.431a.1.1 0 01.018.02.118.118 0 00.017.019.591.591 0 01.076.075.109.109 0 00.02.018.1.1 0 01.019.017.077.077 0 01.01.02.088.088 0 00.01.02c.017.026.031.053.045.078a.9.9 0 01.039.1l.007.021a.5.5 0 01.03.164.1.1 0 000 .023.092.092 0 01.005.027v7.37A1.752 1.752 0 0112.75 14.5zM1.5 6.883v5.87a.253.253 0 00.25.247h11a.253.253 0 00.249-.25V6.883L8.3 10.412a1.737 1.737 0 01-2.1 0zM7.25 1.5a.248.248 0 00-.15.053L2 5.383l5.1 3.83a.253.253 0 00.15.052.245.245 0 00.15-.053l5.1-3.829-5.1-3.83a.248.248 0 00-.15-.053z" transform="translate(.75 .75)"/></svg> <span class="TK-Aside-Menu-Button-Text">Contact Us</span></a></li><li class="TK-Aside-Menu-Item TK-bn"><a href="/download" class="TK-Button TK-Button--CTA">Get A Free Trial</a></li></ul></div><div class="TK-Drawer-Extension"></div><div class="TK-Aside TK--Mobile"><ul class="TK-Aside-Menu"><li class="TK-Aside-Menu-Item TK-Aside-Menu-Button--Search"><a href="/search" class="TK-Aside-Menu-Link js-tlrk-nav-search-link" title="Search" data-match-exact-path><svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="15" height="15" viewBox="0 0 512 512" xml:space="preserve"><path d="M504.4,464L378.9,338.5c25.6-34.8,40.8-77.7,40.8-124.2c0-115.7-94.1-209.8-209.8-209.8C94.2,4.5,0,98.6,0,214.3 C0,330,94.2,424.1,209.9,424.1c50.5,0,96.9-17.9,133.1-47.8l124.5,124.5c5.1,5.1,11.8,7.6,18.4,7.6s13.3-2.5,18.4-7.6 C514.6,490.7,514.6,474.2,504.4,464z M52.2,214.3c0-87,70.7-157.7,157.7-157.7s157.7,70.7,157.7,157.7c0,41-15.7,78.3-41.4,106.4 c-0.3,0.3-0.7,0.6-1,0.9c-0.7,0.7-1.3,1.4-1.9,2.2c-28.7,29.7-68.9,48.2-113.4,48.2C122.9,372,52.2,301.3,52.2,214.3z"></path></svg></a></li><li class="TK-Aside-Menu-Item"><button type="button" aria-label="Main Navigation" class="TK-Aside-Menu-Button TK-Aside-Menu-Button--Toggle-Drawer" id="js-tlrk-nav-drawer-button"><svg id="menu" viewBox="0 0 100 80" class="WUG-Svg WUG-Svg-Hamburger" width="22" height="16"><line x1="10" y1="40" x2="90" y2="40"></line><line x1="10" y1="40" x2="90" y2="40"></line><line x1="10" y1="40" x2="90" y2="40"></line></svg></button></li></ul></div></div></section><button type="button" class="TK-Nav-Overlay" id="js-tlrk-nav-overlay">close mobile menu</button></nav><script async nomodule src="https://d6vtbcy3ong79.cloudfront.net/telerik-navigation/3.5.52/js/index.min.js"></script><script async type="module" src="https://d6vtbcy3ong79.cloudfront.net/telerik-navigation/3.5.52/js/index.min.mjs"></script>

    <div class="u-f1">
        


<div class="header">
    <div class="container u-pt20 u-pb20">
        <a class="breadcrumb e2e-forum-breadcrumb-h" href="/forums">
            <svg xmlns="http://www.w3.org/2000/svg" class="i-arrow-left" viewBox="0 0 10 10">
	<polygon points="4.44 10 0 5 4.44 0 5.21 0.7 1.85 4.48 10 4.48 10 5.52 1.85 5.52 5.21 9.3 4.44 10" />
</svg>
            Telerik Forums
        </a>
			
		 
    </div>
</div>


<div id="thread-details">
    

<div class="thread-migrated-mob d-block d-lg-none">
	<div class="container">
		This is a migrated thread and some comments may be shown as answers.
	</div>
</div>
<div class="sub-header">
    <div class="container">
        <div class="u-mt6">
            <div class="thread-heading">
                <h1 class="e2e-thread-title u-mr15 u-mob-mr0">Virtual mode &#x2B; custom cell DataTemplate = problems</h1>
                
            </div>
        </div>

        <div class="u-mt20 text-light">
            <svg xmlns="http://www.w3.org/2000/svg" class="i-thread-answers e2e-th-i e2e-thi-ha" viewBox="0 0 16 16">
	<path d="M1.8,16l2.1-3.23a7,7,0,1,1,5.88,1.1ZM8,.83A6.37,6.37,0,0,0,6.43,1,6.25,6.25,0,0,0,4.67,12.3l.35.24-1.35,2.1,5.91-1.57A6.23,6.23,0,0,0,8,.83ZM5.5,5h6a.5.5,0,0,1,.5.5h0a.5.5,0,0,1-.5.5h-6A.5.5,0,0,1,5,5.5H5A.5.5,0,0,1,5.5,5Zm0,2h5a.5.5,0,0,1,.5.5h0a.5.5,0,0,1-.5.5h-5A.5.5,0,0,1,5,7.5H5A.5.5,0,0,1,5.5,7Zm0,2h3a.5.5,0,0,1,.5.5H9a.5.5,0,0,1-.5.5h-3A.5.5,0,0,1,5,9.5H5A.5.5,0,0,1,5.5,9Z" />
</svg><span class="u-vam mr-2 e2e-thread-answers">18 Answers</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="i-thread-views" viewBox="0 0 16 16">
    <path data-name="views 16" d="M8,4C4.17,4,1.05,6.9.19,7.8a.65.65,0,0,0,0,.91h0c.86.89,4,3.8,7.81,3.8s7-2.9,7.81-3.8a.65.65,0,0,0,0-.91h0C15,6.91,11.83,4,8,4Zm0,7.61c-3.31,0-6.15-2.52-7-3.36.86-.84,3.7-3.36,7-3.36s6.15,2.52,7,3.36C14.15,9.09,11.31,11.61,8,11.61ZM5.06,8.25A2.94,2.94,0,1,0,8,5.28a2.94,2.94,0,0,0-2.94,3ZM8.84,6.52A.89.89,0,1,1,8,7.41H8a.88.88,0,0,1,.88-.89Z" />
</svg><span class="u-vam mr-2 e2e-thread-views">884 Views</span>
        </div>
    </div>
</div>
<div class="thread-mob-tags d-block d-lg-none">
    <div class="container">
            <span class="tag selected u-mr5 u-mb5">
                GridView
            </span>
    </div>
</div>

<div class="container u-pr">
    <div class="row no-gutters">
        <div class="thread-migrated d-none d-lg-block e2e-thread-migrated">
            This is a migrated thread and some comments may be shown as answers.
        </div>
        <div class="col-main-content u-mb50">
            <div class="u-pr30 u-pt30 u-mob-pr0 u-mob-pt20">
                <div class="row no-gutters mb-5 answer-separator u-mob-bb0">
                    <div id="270345" class="col answer-container e2e-thread-question">
                        <div class="row no-gutters">
                            <span class="u-mb10 thread-lock-label e2e-thread-locked">This question is locked. New answers and comments are not allowed.</span>
                        </div>
                        <div class="edit-post-popup">
                            <div class="row no-gutters justify-content-between u-mb10 text-light post">
                                <div class="col-9 col-sm-10 col-lg-10 messageby-col align-items-start align-content-lg-center">
                                    <div class="messageby-col achievements-tooltip-zone e2e-msg-author">
                                        <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                        <div class="achievements-tooltip-anchor">
                                            <a class="username d-lg-inline-block d-none e2e-username" href="/forums/profile/8d76c6c5-83bf-4f50-8095-54150a65b25b">Eugen Rata</a>
                                            
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                        </div>
                                    </div>
                                    <div class="modified d-inline-block d-lg-block e2e-msg-action">
                                        <a class="username d-lg-none" href="/forums/profile/8d76c6c5-83bf-4f50-8095-54150a65b25b">Eugen Rata</a>
                                        asked on <span class="local-datetime e2e-th-date" data-timestamp="1262478015163"><span class="u-dib">03 Jan 2010,&nbsp;</span><span class="u-dib">12:20 AM</span></span>
                                    </div>
                                </div>
                                <div class="col-auto actions-container">
                                    
                                    <a href="#"
                                       class="social-care e2e-msg-care"
                                       data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#270345"
                                       data-title="Share this question"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                </div>
                            </div>
                            <div id="msg-content-1048473">
                                <div>
                                    
                                    <div class="pb-3 u-mr20 msg-content e2e-msg-text">I have such a code for the grid I'm using<div><div></div><span><div style="overflow-x: auto; overflow-y: auto; background-color: rgba(255, 255, 255, 1); border: 1px solid rgba(127, 157, 185, 1); line-height: 100% !important; font-family: &quot;courier new&quot;; font-size: 11px" class="tFormatCodeBlock supportThreadCodeBlock"><table cellpadding="0" cellspacing="0" style="width: 99%; margin: 2px 0; border-collapse: collapse; border-bottom: 0 solid rgba(238, 238, 238, 1); background-color: rgba(255, 255, 255, 1); border-top-width: 0; border-right-width: 0; border-left-width: 0">    <colgroup><col style="font-family: &quot;courier new&quot;; font-size: 11px; padding-left: 10px; border-bottom: 1px solid rgba(247, 247, 247, 1); white-space: nowrap">    </colgroup><tbody>        <tr>            <td><span style="font-size: 11px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: rgba(0, 0, 255, 1)">&lt;</span><span style="font-size: 11px">telerik:GridViewDataColumn&nbsp;</span><span style="color: rgba(255, 0, 0, 1)">Header</span><span style="font-size: 11px">=</span><span style="color: rgba(0, 0, 255, 1)">"Type"</span><span style="font-size: 11px">&nbsp;</span><span style="color: rgba(255, 0, 0, 1)">DataMemberBinding</span><span style="font-size: 11px">=</span><span style="color: rgba(0, 0, 255, 1)">"{Binding&nbsp;TypeCombo}"</span><span style="font-size: 11px">&gt;&nbsp;</span></td>        </tr>        <tr>            <td style="background-color: rgba(247, 247, 247, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(0, 0, 255, 1)">&lt;</span><span style="font-size: 11px">telerik:GridViewDataColumn.CellTemplate</span><span style="color: rgba(0, 0, 255, 1)">&gt;</span><span style="font-size: 11px">&nbsp;</span></td>        </tr>        <tr>            <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(0, 0, 255, 1)">&lt;</span><span style="font-size: 11px">DataTemplate</span><span style="color: rgba(0, 0, 255, 1)">&gt;</span><span style="font-size: 11px">&nbsp;</span></td>        </tr>        <tr>            <td style="background-color: rgba(247, 247, 247, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(0, 0, 255, 1)">&lt;</span><span style="font-size: 11px">telerikInput:RadComboBox&nbsp;</span><span style="color: rgba(255, 0, 0, 1)">ItemsSource</span><span style="font-size: 11px">=</span><span style="color: rgba(0, 0, 255, 1)">"{Binding&nbsp;TypeCombo.ItemsSource}"</span><span style="font-size: 11px">&nbsp;&nbsp;</span></td>        </tr>        <tr>            <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(255, 0, 0, 1)">SelectedIndex</span><span style="font-size: 11px">=</span><span style="color: rgba(0, 0, 255, 1)">"{Binding&nbsp;TypeCombo.SelectedIndex,&nbsp;Mode=TwoWay}"</span><span style="font-size: 11px">&nbsp;&nbsp;</span></td>        </tr>        <tr>            <td style="background-color: rgba(247, 247, 247, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(255, 0, 0, 1)">IsEnabled</span><span style="font-size: 11px">=</span><span style="color: rgba(0, 0, 255, 1)">"{Binding&nbsp;IsComboTypeEnabled}"</span><span style="font-size: 11px">/&gt;&nbsp;</span></td>        </tr>        <tr>            <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(0, 0, 255, 1)">&lt;/</span><span style="font-size: 11px">DataTemplate</span><span style="color: rgba(0, 0, 255, 1)">&gt;</span><span style="font-size: 11px">&nbsp;</span></td>        </tr>        <tr>            <td style="background-color: rgba(247, 247, 247, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(0, 0, 255, 1)">&lt;/</span><span style="font-size: 11px">telerik:GridViewDataColumn.CellTemplate</span><span style="color: rgba(0, 0, 255, 1)">&gt;</span><span style="font-size: 11px">&nbsp;</span></td>        </tr>        <tr>            <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgba(0, 0, 255, 1)">&lt;/</span><span style="font-size: 11px">telerik:GridViewDataColumn</span><span style="color: rgba(0, 0, 255, 1)">&gt;</span><span style="font-size: 11px">&nbsp;</span></td>        </tr>        <tr>            <td style="background-color: rgba(247, 247, 247, 1)">&nbsp;</td>        </tr>    </tbody></table></div></span><div><br></div><div>when&nbsp;EnableRowVirtualization is set to true (which is by default) that creates a lots of issues.</div><div>When scrolling the grid, up &amp; down, cause ComboBoxes are reused, they get filled with wrong values and because of that when TypeCombo.SelectedIndex get's called I get a lot of "Index out of bounds" exception. If I set&nbsp;EnableRowVirtualization=false, everything works as expected.&nbsp;</div><div>There are 15 such columns with custom CellTemplate and DataTemplate.</div><div><br></div><div>Something must be done here, or at least make by default that&nbsp;EnableRowVirtualization is false, unless you expect that most of people don't use Lookup comboboxes in their grids, that is very false for most of LOB applications.</div><div>And by the way, I do have like 40 rows, and when&nbsp;EnableRowVirtualization=true, the scrolling is much slower than virtual mode is set to false.</div><div><br></div><div>P.S. I'm using latest internal build available as of 1/2/2010.</div><div><br></div></div></div>
                                </div>
                                
                                <div class="loader-container centered" style="display: none">
                                    <div class="loader"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="u-mt10 e2e-question-comments">
                            
<div id="comments-1048473" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                        </div>
                    </div>
                </div>

                <div class="row no-gutters mt-1 u-mb35 answer-separator u-mob-bb0 answer-stats justify-content-between align-items-center">
                    <div class="col-auto">
                        <h2 class="e2e-thread-answers-title">18 Answers<span id="accpetedHeading" class="u-dn">, 1 is accepted</span></h2>
                    </div>
                    <div class="col-auto text-light thread-sort-container">
                        <form method="get"
                              action="/forums/virtual-mode-custom-cell-datatemplate-problems/answers"
                              autocomplete="off"
                              data-ajax="true"
                              data-ajax-update="#thread-details"
                              data-ajax-loading="#answers-list-loader"
                              data-ajax-begin="toggleSort"
                              data-ajax-complete="toggleSort"
                              data-ajax-success="initializeThreadMessageHandlers"
                              data-ajax-failure="showDefaultNotificationError">
                            <span class="d-none d-lg-inline">Sort by</span>
							<div class="dropdown-sm">
								<select id="sortDropdown" name="sortBy" class="ml-1 e2e-thread-sort">
									<option >Score</option>
									<option selected>Date</option>
								</select>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="i-sort">
	<path id="sort" d="M7.5,5h8a.5.5,0,0,1,.5.5h0a.5.5,0,0,1-.5.5h-8A.5.5,0,0,1,7,5.5H7A.5.5,0,0,1,7.5,5Zm0,2h7a.5.5,0,0,1,.5.5h0a.5.5,0,0,1-.5.5h-7A.5.5,0,0,1,7,7.5H7A.5.5,0,0,1,7.5,7Zm0,2h5a.5.5,0,0,1,.5.5h0a.5.5,0,0,1-.5.5h-5A.5.5,0,0,1,7,9.5H7A.5.5,0,0,1,7.5,9Zm-2,2.67H3.73V4.33H5.5a.5.5,0,0,0,.4-.8L3.4.2a.5.5,0,0,0-.8,0L.1,3.53a.5.5,0,0,0,.4.8H2.27v7.34H.5a.5.5,0,0,0-.4.8L2.6,15.8a.5.5,0,0,0,.8,0l2.5-3.33A.5.5,0,0,0,5.5,11.67Z" />
</svg>
							</div>
                        </form>
                    </div>
                </div>

                <div class="u-pr">
                        <div id="1052738" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1052738"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1052738"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <span class="username e2e-username support-officer-badge">Milan</span>
                                                    <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1262857826677"><span class="u-dib">07 Jan 2010,&nbsp;</span><span class="u-dib">09:50 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1052738"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1052738">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Hello Eugen Rata,<br>
<p>This is a strange problem. Although the grid reuses some of its elements the DataContext for each item is kept in sync and you should not get incorrect values. Could you please send us your project so that we can observe the issue and try to provide a solution.</p>
<br>
Regards,<br>
 Milan <br>
the Telerik team
<div style="font-size: 10px; padding-top: 10px">
<br>
Instantly find answers to your questions on the new <a style="color: rgba(128, 128, 128, 1)" href="http://www.telerik.com/support" rel="ugc"> Telerik Support Portal</a>.
<br>
Watch a <a style="color: rgba(128, 128, 128, 1)" href="http://tv.telerik.com/telerik/support/using-telerik-support-resources" rel="ugc">video</a> on how to optimize your support resource searches and <a style="color: rgba(128, 128, 128, 1)" href="http://blogs.telerik.com/supportdept/posts/08-12-22/New_support_resources_search_facilities_on_telerik_com.aspx" rel="ugc">check out more tips</a> on the blogs.
</div></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1052738" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1552087" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1552087"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1552087"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/adaf1806-7277-4ca0-8b3b-f7416014df92">Pedro</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1299500272927"><span class="u-dib">07 Mar 2011,&nbsp;</span><span class="u-dib">12:17 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1552087"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1552087">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Hello,<br>
<br>
Do you have a solution ? I have the same issue...<br>
Thanks in advance.<br>
<br>
Best regards,<br>
Pedro</div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1552087" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1552147" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1552147"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1552147"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" onerror="this.src =&#x27;/forums/images/avatarimages/default.gif&#x27;;this.onerror = null" src="/forums/images/adminimages/vladimir.enchev@telerik.com.jpg" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <span class="username e2e-username support-officer-badge">Vlad</span>
                                                    <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1299502076490"><span class="u-dib">07 Mar 2011,&nbsp;</span><span class="u-dib">12:47 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1552147"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1552147">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Hi,
<p>&nbsp;<br>
Since this thread was more than a year ago can you post more info about the problem at your end the the grid version?&nbsp;<br>
<br>
</p>
Kind regards,<br>
 Vlad <br>
the Telerik team
<div class="forumBaloonTop"></div>
<div class="forumBaloon">
Registration for Q1 2011 What’s New Webinar Week is now open. Mark your calendar for the week starting March 21st and <a href="http://www.telerik.com/company/events/q1-2011-release-webinar-week.aspx" rel="ugc">book your seat</a> for a walk through all the exciting stuff we ship with the new release!
</div>
<div class="forumBaloonBottom"></div></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1552147" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1612418" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1612418"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1612418"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/b5ab188d-3e35-4eca-91a4-16b19175ed05">Rupendra</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1303245524993"><span class="u-dib">19 Apr 2011,&nbsp;</span><span class="u-dib">08:38 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1612418"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1612418">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">I am having the same issue as the one above. The scenario is described below:<br>
<br>
The grid ItemSource property&nbsp;is getting bound to a structure which is something like given below<br>
<div class="tFormatCodeBlock supportThreadCodeBlock" style="overflow-y: auto; border: 1px solid rgba(127, 157, 185, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">const</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">string</code> <code style="color: rgba(0, 0, 0, 1)">RowDataPropertyName = </code><code style="color: rgba(0, 0, 255, 1)">"RowData"</code><code style="color: rgba(0, 0, 0, 1)">; </code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">private</code> <code style="color: rgba(0, 0, 0, 1)">ObservableCollection&lt;DetailsGridRowModel&gt; m_RowData; </code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 0, 0, 1)">ObservableCollection&lt;DetailsGridRowModel&gt; RowData </code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">get</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">return</code> <code style="color: rgba(0, 0, 0, 1)">m_RowData; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">set</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">if</code> <code style="color: rgba(0, 0, 0, 1)">(m_RowData == value) </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">return</code><code style="color: rgba(0, 0, 0, 1)">; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 27px !important">&nbsp;</span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">m_RowData = value; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">OnNotifyPropertyChanged(RowDataPropertyName); </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></div>
</div>
<br>
Here each column has a CellTemplate which contains a custom control.<br>
<br>
<div class="tFormatCodeBlock supportThreadCodeBlock" style="overflow-y: auto; border: 1px solid rgba(127, 157, 185, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp; . </code></span></div>
</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp; . </code></span></div>
</code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp; . <br>
<br>
</code></span></div>
</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">int</code> <code style="color: rgba(0, 0, 0, 1)">i = 0; </code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">foreach</code> <code style="color: rgba(0, 0, 0, 1)">(var col </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">in</code> <code style="color: rgba(0, 0, 0, 1)">ColumnsCollection) </code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">GridViewDataColumn column = </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">GridViewDataColumn(); </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">column.CellTemplate = GetDataboundTemplate(i); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 15px !important">&nbsp;</span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 130, 0, 1)">// do something with col here </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 15px !important">&nbsp;</span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">GridView.Columns.Add(column); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">i++; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp; . </code></span></div>
</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp; . </code></span></div>
</code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp; . </code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;</code><span style="margin-left: 3px !important">&nbsp;</span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 15px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 0, 0, 1)">DataTemplate GetDataboundTemplate(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">int</code> <code style="color: rgba(0, 0, 0, 1)">columnIndex) </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">StringBuilder xaml = </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">StringBuilder(); </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">xaml.Append(</code><code style="color: rgba(0, 0, 255, 1)">"&lt;DataTemplate xmlns=\" [namespace] \" xmlns:my=\" [namespace] \"&gt;"</code><code style="color: rgba(0, 0, 0, 1)">); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">xaml.Append(</code><code style="color: rgba(0, 0, 255, 1)">"&lt;my:DetailsGridItemView Context=\"{Binding ColumnData["</code> <code style="color: rgba(0, 0, 0, 1)">+ columnIndex + </code><code style="color: rgba(0, 0, 255, 1)">"]}\" /&gt;"</code><code style="color: rgba(0, 0, 0, 1)">); </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">xaml.Append(</code><code style="color: rgba(0, 0, 255, 1)">"&lt;/DataTemplate&gt;"</code><code style="color: rgba(0, 0, 0, 1)">); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">DataTemplate template = XamlReader.Load(xaml.ToString()) </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">as</code> <code style="color: rgba(0, 0, 0, 1)">DataTemplate; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">return</code> <code style="color: rgba(0, 0, 0, 1)">template; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
</div>
<br>
<br>
The DetailsGridItemView control uses the Context property to render itself correctly.<br>
<br>
<p>The correct behavior for the grid is to bind each row&nbsp;to an instance of DetailsGridRowModel. <strong>When I&nbsp;disable the row and column virtualization everything works fine.<br>
<br>
</strong></p>
However, when I don't have them set explicitly or I enable them explicitly the followng behavior starts happening.<br>
<ul>
    <li>The grid starts to re-bind data to a control that is no-longer visible and hence might be re-used. </li>
    <li>The data that gets picked up for binding is not in the correct order. So the order of items gets lost on sort and that causes a lot of problems and confusion. </li>
</ul>
<br>
Let me illustrate. Say&nbsp; the number of rows visible is 5 and the data for each row is the following list. Lets also assume that the == bars represent the top and bottom edges of the grid control.<br>
<br>
let's say my list is containing the following data
<ul>
    <li>a</li>
    <li>b</li>
    <li>c</li>
    <li>d</li>
    <li>e</li>
    <li>f</li>
    <li>g</li>
    <li>h</li>
    <li>i</li>
    <li>j</li>
</ul>
<p>This is what the user sees then the grid first renders.<br>
<br>
</p>
<p>==================</p>
<ul>
    <li>a </li>
    <li>b </li>
    <li>c </li>
    <li>d </li>
    <li>e </li>
</ul>
<p>==================</p>
<ul>
    <li>?&nbsp;&lt;can't see this right now&gt; </li>
    <li>?&nbsp;&lt;can't see this right now&gt; </li>
    <li>?&nbsp;&lt;can't see this right now&gt; </li>
    <li>?&nbsp;&lt;can't see this right now&gt; </li>
    <li>?&nbsp;&lt;can't see this right now&gt; </li>
</ul>
<p>&nbsp;</p>
Now lets assume that the user scolls to the bottom. The user sees the following.<br>
<br>
<ul>
    <li>? &lt;can't see this right now&gt;&nbsp;&nbsp;</li>
    <li>? &lt;can't see this right now&gt;&nbsp;</li>
    <li>? &lt;can't see this right now&gt;&nbsp;</li>
    <li>? &lt;can't see this right now&gt;&nbsp;</li>
    <li>? &lt;can't see this right now&gt;&nbsp;</li>
</ul>
<p>===================</p>
<ul>
    <li>f </li>
    <li>g </li>
    <li>h </li>
    <li>i </li>
    <li>j </li>
</ul>
===================<br>
<br>
However now when the user scrolls up, the grid does not pick up the items in the list in the correct order. So this is what the user might see (I say might since what gets picked up and bound doesn't seem to be deterministic.)<br>
<br>
<p>==================</p>
<ul>
    <li>g </li>
    <li>i </li>
    <li>a </li>
    <li>b </li>
    <li>d </li>
</ul>
<p>==================</p>
<ul>
    <li>? &lt;can't see this right now&gt; </li>
    <li>? &lt;can't see this right now&gt;&nbsp;&nbsp;</li>
    <li>? &lt;can't see this right now&gt;&nbsp;&nbsp;</li>
    <li>? &lt;can't see this right now&gt;&nbsp;&nbsp;</li>
    <li>? &lt;can't see this right now&gt;&nbsp;&nbsp;</li>
</ul>
<br>
If you notice in the illustration above, I have tried to show that the list shown to the user is not fixed at all. It actually changes and depends on various things which change the timing of the the events firing inside such as
<ul>
    <li>The user stop scrolling and removed the mouse from the scrollbar when he reached at the bottom (as in mousebuttonup event fired or not) and then scrolled up again. </li>
    <li>OR&nbsp;The user scrolled to the bottom and with mouse button still down scrolled to the top slowly or very quickly, etc. </li>
</ul>
<p>&nbsp;<br>
In fact sometimes if the user now scrolls down this is what he might see which absolutly confuses the user.</p>
<ul>
    <li>? &lt;can't see this right now&gt;</li>
    <li>? &lt;can't see this right now&gt;</li>
    <li>? &lt;can't see this right now&gt;</li>
</ul>
<p>==================</p>
<ul>
    <li>b </li>
    <li>d </li>
</ul>
<ul>
    <li>a&nbsp;</li>
    <li>c&nbsp;&nbsp; </li>
    <li>f</li>
</ul>
<p>==================&nbsp;&nbsp; </p>
<ul>
    <li>? &lt;can't see this right now&gt;&nbsp;&nbsp; </li>
    <li>? &lt;can't see this right now&gt;&nbsp;&nbsp;</li>
</ul>
<p><br>
In the real solution I have about 60 rows and 30 are visible on the grid at any time.</p></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1612418" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1618729" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1618729"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1618729"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/b5ab188d-3e35-4eca-91a4-16b19175ed05">Rupendra</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1303759317763"><span class="u-dib">25 Apr 2011,&nbsp;</span><span class="u-dib">07:21 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1618729"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1618729">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">This issue was taken care by the following procedure.<br>
Binding to the properties was done only in XAML (xaml binding and&nbsp;using converters). Code did not relied on&nbsp;binding the properties to different parts of the control.</div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1618729" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1711896" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1711896"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1711896"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/f45bc240-33d0-4b7c-afde-e575f633ea81">Ed</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1309999749363"><span class="u-dib">07 Jul 2011,&nbsp;</span><span class="u-dib">12:49 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1711896"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1711896">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text"><p>Hi,<br>
<br>
I'm currently using version 2010.3.1314.1040.&nbsp;Our gridview typically&nbsp;contains over 1000 rows. One column uses a data template that has a user control, which data binds&nbsp;to a view model.<br>
<br>
With virtualization enabled, we see the behavior described in this thead. The cell value bound changes as you vertically scroll the cell into and out of view. As a former poster describes, the value picked up for binding seems to be re-used or in the wrong order. </p>
<p>&nbsp;</p>
<p>I've also tried on the 2011.1.419 relase, but see the same behavior.<br>
<br>
Please advise.&nbsp;<br>
<br>
<br>
<br>
</p></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1711896" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1712007" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1712007"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1712007"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" onerror="this.src =&#x27;/forums/images/avatarimages/default.gif&#x27;;this.onerror = null" src="/forums/images/adminimages/vladimir.enchev@telerik.com.jpg" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <span class="username e2e-username support-officer-badge">Vlad</span>
                                                    <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1310020954200"><span class="u-dib">07 Jul 2011,&nbsp;</span><span class="u-dib">06:42 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1712007"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1712007">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Hi,
<p>&nbsp;Can you post an example where we can reproduce this with our latest official version - Q1 2011 SP1?</p>
All the best,<br>
 Vlad <br>
the Telerik team
<div class="forumBaloonTop"></div>
<div class="forumBaloon">
<p>
<a href="http://www.telerik.com/support/webinars.aspx" rel="ugc">Register</a> for the <strong>Q2 2011</strong> What's New Webinar Week. Mark your calendar for the week starting July 18th and&nbsp;<a href="http://www.telerik.com/support/webinars.aspx" rel="ugc">book your seat</a> for a walk through of all the exciting stuff we will ship with the new release!</p>
</div>
<div class="forumBaloonBottom"></div></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1712007" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1723527" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1723527"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1723527"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/741898a1-5f9d-425b-8704-50a432c176d6">Calvin</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1310761705647"><span class="u-dib">15 Jul 2011,&nbsp;</span><span class="u-dib">08:28 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1723527"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1723527">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">At your request we have prepared a test application which illustrates the problem which we are experiencing.&nbsp;&nbsp;&nbsp; <br>
<br>
Here is a link to our project files:&nbsp; <a href="http://techsupportfromcal.com/VirtualizationScrollingProblem/VirtualizationScrollingProblem.zip" rel="ugc">http://techsupportfromcal.com/VirtualizationScrollingProblem/VirtualizationScrollingProblem.zip</a><br>
<br>
This is a matter of considerable urgency for us.&nbsp; Thanks for your assistance.&nbsp; <br>
<br>
Quoting from the ReadMe file in our test application: <br>
<pre style="font-family: consolas; background: rgba(255, 255, 255, 1); color: rgba(0, 0, 0, 1); font-size: 13px"><span style="color: rgba(0, 128, 0, 1)">&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;This&nbsp;test&nbsp;application&nbsp;illustrates&nbsp;a&nbsp;problem&nbsp;which&nbsp;we&nbsp;are&nbsp;experiencing&nbsp;with&nbsp;our&nbsp;Telerik&nbsp;Silverlight&nbsp;GridView.&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;The&nbsp;GridView&nbsp;has&nbsp;three&nbsp;columns&nbsp;which&nbsp;display&nbsp;images.&nbsp;The&nbsp;first&nbsp;image&nbsp;column&nbsp;contains&nbsp;a&nbsp;standard&nbsp;Silverlight</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;Image&nbsp;Control.&nbsp;&nbsp;The&nbsp;second&nbsp;column&nbsp;contains&nbsp;a&nbsp;Silverlight&nbsp;User&nbsp;Control&nbsp;which&nbsp;in&nbsp;turn&nbsp;contains&nbsp;a&nbsp;Silverlight&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;Image&nbsp;Control.&nbsp;&nbsp;The&nbsp;third&nbsp;column&nbsp;shows&nbsp;a&nbsp;Silverlight&nbsp;Image&nbsp;Control&nbsp;hosted&nbsp;in&nbsp;a&nbsp;Silverlight&nbsp;Custom&nbsp;Control.</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;As&nbsp;can&nbsp;be&nbsp;seen&nbsp;from&nbsp;running&nbsp;this&nbsp;application,&nbsp;the&nbsp;first&nbsp;two&nbsp;columns&nbsp;display&nbsp;the&nbsp;correct&nbsp;images&nbsp;when</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;scrolling&nbsp;but&nbsp;the&nbsp;third&nbsp;column&nbsp;does&nbsp;not.&nbsp;&nbsp;As&nbsp;you&nbsp;scroll,&nbsp;the&nbsp;images&nbsp;in&nbsp;the&nbsp;third&nbsp;column&nbsp;come&nbsp;from</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;other&nbsp;rows&nbsp;as&nbsp;the&nbsp;Telerik&nbsp;virtualization&nbsp;process&nbsp;reuses&nbsp;some&nbsp;grid&nbsp;components&nbsp;to&nbsp;improve&nbsp;performance.</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;If&nbsp;you&nbsp;set&nbsp;the&nbsp;&nbsp;EnableRowVirtualization&nbsp;property&nbsp;to&nbsp;False,&nbsp;this&nbsp;problem&nbsp;goes&nbsp;away.&nbsp;However,&nbsp;our&nbsp;data</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;sets&nbsp;are&nbsp;often&nbsp;very&nbsp;large&nbsp;and&nbsp;setting&nbsp;this&nbsp;property&nbsp;to&nbsp;False&nbsp;results&nbsp;in&nbsp;an&nbsp;unacceptable&nbsp;degradation</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;in&nbsp;performance.&nbsp;&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;The&nbsp;third&nbsp;image&nbsp;column&nbsp;also&nbsp;contains&nbsp;a&nbsp;textblock&nbsp;which&nbsp;displays&nbsp;the&nbsp;Identifier&nbsp;Name.&nbsp;&nbsp;As&nbsp;can&nbsp;be</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;seen,&nbsp;this&nbsp;value&nbsp;is&nbsp;correct&nbsp;even&nbsp;though&nbsp;the&nbsp;wrong&nbsp;image&nbsp;is&nbsp;usually&nbsp;displayed.&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;We&nbsp;have&nbsp;tried&nbsp;both&nbsp;the&nbsp;User&nbsp;Control&nbsp;and&nbsp;Custom&nbsp;Control&nbsp;approaches&nbsp;in&nbsp;our&nbsp;application&nbsp;and&nbsp;both</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;exhibit&nbsp;this&nbsp;scrolling&nbsp;problem.&nbsp;&nbsp;Of&nbsp;course,&nbsp;our&nbsp;actual&nbsp;controls&nbsp;are&nbsp;much&nbsp;more&nbsp;complex&nbsp;than&nbsp;this&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;sample&nbsp;application.&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;This&nbsp;problem&nbsp;did&nbsp;not&nbsp;occur&nbsp;with&nbsp;the&nbsp;initial&nbsp;release&nbsp;of&nbsp;the&nbsp;Telerik&nbsp;controls&nbsp;from&nbsp;2010&nbsp;Q3.&nbsp;</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;We&nbsp;first&nbsp;noticed&nbsp;this&nbsp;problem&nbsp;after&nbsp;applying&nbsp;SP1&nbsp;to&nbsp;the&nbsp;Q3&nbsp;release.&nbsp;&nbsp;This&nbsp;test&nbsp;application</span>
<span style="color: rgba(0, 128, 0, 1)">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;as&nbsp;requested&nbsp;by&nbsp;Telerik&nbsp;support&nbsp;uses&nbsp;the&nbsp;Q1&nbsp;2011&nbsp;release.&nbsp;&nbsp;<br><br><br><br>&nbsp;&nbsp;&nbsp;&nbsp;<br></span></pre></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1723527" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1731502" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1731502"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1731502"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/741898a1-5f9d-425b-8704-50a432c176d6">Calvin</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1311296385493"><span class="u-dib">22 Jul 2011,&nbsp;</span><span class="u-dib">12:59 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1731502"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1731502">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Could you please advise us regarding any progress in examining this issue. &nbsp; &nbsp;We are actively working on finding a satisfactory work around but so far we have not developed an acceptable solution. &nbsp;<br>
<br>
Thanks. &nbsp;</div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1731502" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1731695" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1731695"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1731695"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" onerror="this.src =&#x27;/forums/images/avatarimages/default.gif&#x27;;this.onerror = null" src="/forums/images/adminimages/vladimir.enchev@telerik.com.jpg" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <span class="username e2e-username support-officer-badge">Vlad</span>
                                                    <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1311322391193"><span class="u-dib">22 Jul 2011,&nbsp;</span><span class="u-dib">08:13 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1731695"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1731695">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Hi,
<p>&nbsp;We've checked your scenario with the standard Microsoft&nbsp;Silverlight&nbsp;DataGrid and the behavior is exactly the same. It seems that the problem is in your&nbsp;BasicStructure component - please verify this!</p>
Best wishes,<br>
 Vlad <br>
the Telerik team
<div class="forumBaloonTop"></div>
<div class="forumBaloon">
<p>
<a href="http://www.telerik.com/support/webinars.aspx" rel="ugc">Register</a> for the <strong>Q2 2011</strong> What's New Webinar Week. Mark your calendar for the week starting July 18th and&nbsp;<a href="http://www.telerik.com/support/webinars.aspx" rel="ugc">book your seat</a> for a walk through of all the exciting stuff we will ship with the new release!</p>
</div>
<div class="forumBaloonBottom"></div></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1731695" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1733015" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1733015"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1733015"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/741898a1-5f9d-425b-8704-50a432c176d6">Calvin</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1311387676350"><span class="u-dib">23 Jul 2011,&nbsp;</span><span class="u-dib">02:21 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1733015"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1733015">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Thanks for the update.<br>
<br>
1. Our application uses the Telerik Grid Control, not the Microsoft Grid Control and at least as of this point we are not looking to switch. <br>
<br>
2. I would be happy to review any suggestions which you have regarding a possible problem with the BasicStructure component in my test application.&nbsp; However, for purpose of creating this test application I made this component as simple as possible (our actual application is much more complicated).&nbsp; It consists of nothing more than a custom control with two dependency properties and a UI consisting of a textblock and an image control.&nbsp; The textblock refreshes correctly but the image control does not.&nbsp; I don't mind at all removing the textblock since we don't actually have one of those in our real application but I can't remove the image control because that is the whole point of this column in our application. &nbsp;<br>
<br>
3.&nbsp; This test application works just fine with your Q3 2010 controls (pre SP1).&nbsp; Here's a link: <br>
&nbsp; <a href="http://techsupportfromcal.com/VirtualizationScrollingProblem/VirtualizationScrollingProblemQ32010.zip" rel="ugc">http://techsupportfromcal.com/VirtualizationScrollingProblem/VirtualizationScrollingProblemQ32010.zip</a><br>
If this test application works just fine with an earlier version of your controls but is broken with the current version of your controls, I would conclude that you must have changed something in how your controls work.&nbsp; That is what we would like you to check into. &nbsp;<br>
<br>
4.&nbsp; In our actual application we have two columns which are causing this problem -- one with an image and the other with a list box.&nbsp; It didn't seem necessary to illustrate both problems since a fix for one of them will most likely provide a solution for both of them.&nbsp; We have tested many different variations of these controls in our application (both Silverlight UserControls and Silverlight Custom Controls) and they all have this same problem.&nbsp;</div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1733015" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1733442" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1733442"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1733442"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" onerror="this.src =&#x27;/forums/images/avatarimages/default.gif&#x27;;this.onerror = null" src="/forums/images/adminimages/vladimir.enchev@telerik.com.jpg" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <span class="username e2e-username support-officer-badge">Vlad</span>
                                                    <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1311579437530"><span class="u-dib">25 Jul 2011,&nbsp;</span><span class="u-dib">07:37 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1733442"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1733442">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Hello,
<p>&nbsp;Here is how to change your custom control + converter to fix this:<br>
</p><div class="tFormatCodeBlock supportThreadCodeBlock" style="border: 1px solid rgba(127, 157, 185, 1); overflow-y: auto">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Style</code> <code style="color: rgba(128, 128, 128, 1)">TargetType</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"CustomControls:BasicStructure"</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Setter</code> <code style="color: rgba(128, 128, 128, 1)">Property</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Background"</code> <code style="color: rgba(128, 128, 128, 1)">Value</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"White"</code> <code style="color: rgba(0, 0, 0, 1)">/&gt;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Setter</code> <code style="color: rgba(128, 128, 128, 1)">Property</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Template"</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Setter.Value</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">ControlTemplate</code> <code style="color: rgba(128, 128, 128, 1)">TargetType</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"CustomControls:BasicStructure"</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 60px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Grid</code> <code style="color: rgba(128, 128, 128, 1)">x:Name</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"LayoutRoot"</code> <code style="color: rgba(128, 128, 128, 1)">Background</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"{TemplateBinding Background}"</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 84px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">StackPanel</code> <code style="color: rgba(128, 128, 128, 1)">Orientation</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Vertical"</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><code>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</code><span style="margin-left: 96px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">TextBlock</code> <code style="color: rgba(128, 128, 128, 1)">x:Name</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"txbImageName"</code>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</span><br>
</div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 108px !important"><code style="color: rgba(128, 128, 128, 1)">Text</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"{Binding RelativeSource={RelativeSource TemplatedParent},&nbsp; Path=ImageName}"</code>&nbsp;&nbsp;&nbsp; <code style="color: rgba(0, 0, 0, 1)">/&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 96px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Image</code> <code style="color: rgba(128, 128, 128, 1)">x:Name</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"StructureImage"</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 117px !important"><code style="color: rgba(0, 0, 0, 1)">Source="{Binding RelativeSource={RelativeSource TemplatedParent}, </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 156px !important"><code style="color: rgba(128, 128, 128, 1)">Path</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">ImageName</code><code style="color: rgba(0, 0, 0, 1)">, Converter={StaticResource imageNameToImageConverter}}"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 120px !important"><code style="color: rgba(128, 128, 128, 1)">Height</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"100"</code> <code style="color: rgba(128, 128, 128, 1)">Width</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"100"</code>&nbsp; <code style="color: rgba(0, 0, 0, 1)">/&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 84px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">StackPanel</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 60px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Grid</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">ControlTemplate</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Setter.Value</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Setter</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Style</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
</div>
<br>
<div class="tFormatCodeBlock supportThreadCodeBlock" style="border: 1px solid rgba(127, 157, 185, 1); overflow-y: auto">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">class</code> <code style="color: rgba(0, 0, 0, 1)">BasicStructureToImageConverter&nbsp; :IValueConverter</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">Convert(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">value, Type targetType, </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">parameter, System.Globalization.CultureInfo culture)</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">string</code> <code style="color: rgba(0, 0, 0, 1)">imageName = value </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">as</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">string</code><code style="color: rgba(0, 0, 0, 1)">;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">Uri uri = </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">Uri(@</code><code style="color: rgba(0, 0, 255, 1)">"<a href="http://localhost" rel="ugc">http://localhost</a>:6449"</code> <code style="color: rgba(0, 0, 0, 1)">+ </code><code style="color: rgba(0, 0, 255, 1)">"/images/"</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 69px !important"><code style="color: rgba(0, 0, 0, 1)">+ HttpUtility.UrlEncode(imageName) + </code><code style="color: rgba(0, 0, 255, 1)">".png"</code><code style="color: rgba(0, 0, 0, 1)">, UriKind.Absolute);</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">return</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">BitmapImage(uri);</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">ConvertBack(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">value, Type targetType, </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">parameter, System.Globalization.CultureInfo culture)</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">throw</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">NotImplementedException();</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
</div>
<p></p>
All the best,<br>
 Vlad <br>
the Telerik team
<div class="forumBaloonTop"></div>
<div class="forumBaloon">
<p>
<a href="http://www.telerik.com/support/webinars.aspx" rel="ugc">Register</a> for the <strong>Q2 2011</strong> What's New Webinar Week. Mark your calendar for the week starting July 18th and&nbsp;<a href="http://www.telerik.com/support/webinars.aspx" rel="ugc">book your seat</a> for a walk through of all the exciting stuff we will ship with the new release!</p>
</div>
<div class="forumBaloonBottom"></div></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1733442" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1736879" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1736879"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1736879"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/741898a1-5f9d-425b-8704-50a432c176d6">Calvin</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1311718849093"><span class="u-dib">26 Jul 2011,&nbsp;</span><span class="u-dib">10:20 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1736879"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1736879">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Thanks for your response. &nbsp;<br>
<br>
I guess that one of the disadvantages of simplifying our test application to remove most of the complexities of our real application is that some of the constraints of our application are no longer clear.&nbsp; Your proposed solution would work nicely in our case if we needed only a simple string in our value converter.&nbsp; In our actual application, however, we need four items of data inside the value converter: <br>
<br>
&nbsp;&nbsp; &nbsp;1.&nbsp;&nbsp;&nbsp;a string which via some business logic is converted into the name of the file for our image, <br>
<br>
&nbsp;&nbsp; &nbsp;2.&nbsp;&nbsp;&nbsp;a specification of which default image to use if there is no image corresponding to that file name, <br>
<br>
&nbsp;&nbsp; &nbsp;3.&nbsp;&nbsp;&nbsp;the height and <br>
<br>
&nbsp;&nbsp; &nbsp;4.&nbsp;&nbsp;&nbsp;the width of the desired image.<br>
<br>
That is the reason why our real application and the test application built to simulate the real application, pass in an object which can include each of those four values as properties.</div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1736879" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1757298" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1757298"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1757298"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/741898a1-5f9d-425b-8704-50a432c176d6">Calvin</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1313031755360"><span class="u-dib">11 Aug 2011,&nbsp;</span><span class="u-dib">03:02 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1757298"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1757298">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">In the absence of a fix for this problem could we just get a confirmation that if we need to pass an object to our value converter, for versions of your RadGridView later than 2010 Q3, there is no simple solution to this virtualization-scrolling problem.&nbsp; <br>
<br>
Thanks.</div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1757298" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="1777907" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="1777907"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="1777907"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/d5934430-e1a7-4c53-aefd-0efe8e1439a4">Mikle</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1314351016043"><span class="u-dib">26 Aug 2011,&nbsp;</span><span class="u-dib">09:30 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#1777907"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-1777907">
                                        <div>
                                            <div class="row no-gutters u-mb10">
                                                    <div class="attachment col-12 u-mb10 e2e-msg-att"
                                                         data-attachmentId="295522"
                                                         data-filesize=""
                                                         data-extension=".JPG">
                                                        
                                                        <span><svg x="0px" y="0px" width="512px" height="512px" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" class="i-file-image">
    <path d="M298.7,385.2c0,0-26.5-97.2-85.6-97.2s-85,128-85,128h256c0,0-11.9-78.7-42.7-78.7S298.7,385.2,298.7,385.2z M352,32H96c-17.7,0-32,14.3-32,32v384c0,17.7,14.3,32,32,32h320c17.7,0,32-14.3,32-32V128L352,32z M416,448H96V64h224v96h96V448z M288,256c0,17.7,14.3,32,32,32s32-14.3,32-32s-14.3-32-32-32S288,238.3,288,256z" />
</svg></span>
                                                        
                                                        
                                                        <a href="/forums/attachments/295522" target="_blank" class="u-ml10 u-vam e2e-att-name" >GridViewCellTemplateBug.JPG</a>
                                                    </div>
                                            </div>
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">I have a little example of this problem.<br>
Sample application generates some data with selected checkbox in first column.<br>
Run application. Deselect checkbox in first row. Than scroll down using keyboard. Note selection bar in some rows and wrongly deselected checkboxes.<br>
<br>
XAML:<br>
<div class="tFormatCodeBlock supportThreadCodeBlock" style="overflow-y: auto; border: 1px solid rgba(127, 157, 185, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">UserControl</code> <code style="color: rgba(128, 128, 128, 1)">x:Class</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"GridViewCellTemplateBug.MainPage"</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(128, 128, 128, 1)">xmlns</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"<a href="http://schemas.microsoft.com/winfx/2006/xaml/presentation" rel="ugc">http://schemas.microsoft.com/winfx/2006/xaml/presentation</a>"</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(128, 128, 128, 1)">xmlns:x</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"<a href="http://schemas.microsoft.com/winfx/2006/xaml" rel="ugc">http://schemas.microsoft.com/winfx/2006/xaml</a>"</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(128, 128, 128, 1)">xmlns:d</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"<a href="http://schemas.microsoft.com/expression/blend/2008" rel="ugc">http://schemas.microsoft.com/expression/blend/2008</a>"</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(128, 128, 128, 1)">xmlns:mc</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"<a href="http://schemas.openxmlformats.org/markup-compatibility/2006" rel="ugc">http://schemas.openxmlformats.org/markup-compatibility/2006</a>"</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(128, 128, 128, 1)">xmlns:telerik</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"<a href="http://schemas.telerik.com/2008/xaml/presentation" rel="ugc">http://schemas.telerik.com/2008/xaml/presentation</a>"</code>&nbsp;</span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(128, 128, 128, 1)">mc:Ignorable</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"d"</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(128, 128, 128, 1)">d:DesignHeight</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"300"</code> <code style="color: rgba(128, 128, 128, 1)">d:DesignWidth</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"400"</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;</code><span style="margin-left: 3px !important">&nbsp;</span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Grid</code> <code style="color: rgba(128, 128, 128, 1)">x:Name</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"LayoutRoot"</code> <code style="color: rgba(128, 128, 128, 1)">Background</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"White"</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:RadGridView</code> <code style="color: rgba(128, 128, 128, 1)">x:Name</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"rgvProducts"</code> <code style="color: rgba(128, 128, 128, 1)">Grid.Row</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"1"</code> <code style="color: rgba(128, 128, 128, 1)">Margin</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"0,10,0,5"</code> <code style="color: rgba(128, 128, 128, 1)">CanUserFreezeColumns</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"False"</code> <code style="color: rgba(128, 128, 128, 1)">GridLinesVisibility</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Both"</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 72px !important"><code style="color: rgba(128, 128, 128, 1)">HorizontalAlignment</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Stretch"</code> <code style="color: rgba(128, 128, 128, 1)">VerticalAlignment</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Stretch"</code> <code style="color: rgba(128, 128, 128, 1)">FontSize</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"10"</code> <code style="color: rgba(128, 128, 128, 1)">FontWeight</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Normal"</code> <code style="color: rgba(128, 128, 128, 1)">Height</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Auto"</code> <code style="color: rgba(128, 128, 128, 1)">ShowGroupPanel</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"False"</code>&nbsp;</span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 72px !important"><code style="color: rgba(128, 128, 128, 1)">IsFilteringAllowed</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"True"</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 72px !important"><code style="color: rgba(128, 128, 128, 1)">AutoGenerateColumns</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"False"</code> <code style="color: rgba(128, 128, 128, 1)">IsReadOnly</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"False"</code> <code style="color: rgba(128, 128, 128, 1)">CanUserSelect</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"False"</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:RadGridView.Columns</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:GridViewDataColumn</code> <code style="color: rgba(128, 128, 128, 1)">Header</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Select"</code> <code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 60px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:GridViewDataColumn.CellTemplate</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 72px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">DataTemplate</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 84px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">CheckBox</code> <code style="color: rgba(128, 128, 128, 1)">IsChecked</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"{Binding Selected}"</code> <code style="color: rgba(128, 128, 128, 1)">IsEnabled</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"True"</code> <code style="color: rgba(128, 128, 128, 1)">HorizontalAlignment</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Center"</code> <code style="color: rgba(0, 0, 0, 1)">/&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 72px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">DataTemplate</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 60px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:GridViewDataColumn.CellTemplate</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:GridViewDataColumn</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:GridViewDataColumn</code> <code style="color: rgba(128, 128, 128, 1)">Header</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"Description"</code> <code style="color: rgba(128, 128, 128, 1)">UniqueName</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"SKUDescription"</code> <code style="color: rgba(128, 128, 128, 1)">IsReadOnly</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"True"</code> <code style="color: rgba(0, 0, 0, 1)">/&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:RadGridView.Columns</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">telerik:RadGridView</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">Grid</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">UserControl</code><code style="color: rgba(0, 0, 0, 1)">&gt; </code></span></div>
</div>
<br>
Code:<br>
<div class="tFormatCodeBlock supportThreadCodeBlock" style="overflow-y: auto; border: 1px solid rgba(127, 157, 185, 1)">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">using</code> <code style="color: rgba(0, 0, 0, 1)">System.Collections.Generic; </code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">using</code> <code style="color: rgba(0, 0, 0, 1)">System.Windows.Controls; </code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">using</code> <code style="color: rgba(0, 0, 0, 1)">System.ComponentModel; </code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;</code><span style="margin-left: 3px !important">&nbsp;</span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">namespace</code> <code style="color: rgba(0, 0, 0, 1)">GridViewCellTemplateBug </code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">partial</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">class</code> <code style="color: rgba(0, 0, 0, 1)">MainPage : UserControl </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 0, 0, 1)">MainPage() </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">InitializeComponent(); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">ProductCollection itemList = </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">ProductCollection(); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">for</code> <code style="color: rgba(0, 0, 0, 1)">(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">int</code> <code style="color: rgba(0, 0, 0, 1)">i = 0; i &lt; 100; i++) </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">Product item = </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">Product(); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">item.Selected = </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">true</code><code style="color: rgba(0, 0, 0, 1)">; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">item.SKUDescription = </code><code style="color: rgba(0, 0, 255, 1)">"Description"</code> <code style="color: rgba(0, 0, 0, 1)">+ i.ToString() + </code><code style="color: rgba(0, 0, 255, 1)">"&nbsp;&nbsp; number"</code> <code style="color: rgba(0, 0, 0, 1)">+ i.ToString() + i.ToString(); </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">itemList.Add(item); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">rgvProducts.ItemsSource = itemList; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;</code><span style="margin-left: 3px !important">&nbsp;</span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">class</code> <code style="color: rgba(0, 0, 0, 1)">Product : </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code><code style="color: rgba(0, 0, 0, 1)">, INotifyPropertyChanged </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">private</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">bool</code> <code style="color: rgba(0, 0, 0, 1)">_Selected; </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">string</code> <code style="color: rgba(0, 0, 0, 1)">SKUDescription { </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">get</code><code style="color: rgba(0, 0, 0, 1)">; </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">set</code><code style="color: rgba(0, 0, 0, 1)">; } </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">bool</code> <code style="color: rgba(0, 0, 0, 1)">Selected </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">get</code> <code style="color: rgba(0, 0, 0, 1)">{ </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">return</code> <code style="color: rgba(0, 0, 0, 1)">_Selected; } </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">set</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">_Selected = value; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">NotifyPropertyChanged(</code><code style="color: rgba(0, 0, 255, 1)">"Selected"</code><code style="color: rgba(0, 0, 0, 1)">); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">event</code> <code style="color: rgba(0, 0, 0, 1)">PropertyChangedEventHandler PropertyChanged; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">void</code> <code style="color: rgba(0, 0, 0, 1)">NotifyPropertyChanged(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">string</code> <code style="color: rgba(0, 0, 0, 1)">propertyName) </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">if</code> <code style="color: rgba(0, 0, 0, 1)">(PropertyChanged != </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">null</code><code style="color: rgba(0, 0, 0, 1)">) </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">PropertyChanged(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">this</code><code style="color: rgba(0, 0, 0, 1)">, </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">PropertyChangedEventArgs(propertyName)); </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">class</code> <code style="color: rgba(0, 0, 0, 1)">ProductCollection : List&lt;Product&gt; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 0, 0, 1)">ProductCollection() : </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">base</code><code style="color: rgba(0, 0, 0, 1)">() { } </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 0, 0, 1)">ProductCollection(Product[] items) </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">: </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">base</code><code style="color: rgba(0, 0, 0, 1)">() </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">if</code> <code style="color: rgba(0, 0, 0, 1)">(items != </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">null</code><code style="color: rgba(0, 0, 0, 1)">) </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">foreach</code> <code style="color: rgba(0, 0, 0, 1)">(Product item </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">in</code> <code style="color: rgba(0, 0, 0, 1)">items) </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">{ </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 60px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">this</code><code style="color: rgba(0, 0, 0, 1)">.Add(item); </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">}; </code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">} </code></span></div>
</div>
<br></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-1777907" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="3138410" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="3138410"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="3138410"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/53fd9040-d006-4bd1-9859-abbe1ee7e00f">Autolog</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1401801774347"><span class="u-dib">03 Jun 2014,&nbsp;</span><span class="u-dib">01:22 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#3138410"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-3138410">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">I ran into the same issue with a radiobutton, and short of extending GridViewColumn into my own GridViewRadioButtonColumn, I solved it by creating a behavior which refreshes the binding on the radio buttons&nbsp;manually when the layout updates. It could easily be changed into a behavior for a checkbox:<br>
<br>
<div class="reCodeBlock" style="border: 1px solid rgba(127, 157, 185, 1); border-image: none">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">class</code> <code style="color: rgba(0, 0, 0, 1)">VirtualizedRadioButtonBehavior : Behavior&lt;RadioButton&gt;</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">protected</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">override</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">void</code> <code style="color: rgba(0, 0, 0, 1)">OnAttached()</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">AssociatedObject.LayoutUpdated += AssociatedObject_LayoutUpdated;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">base</code><code style="color: rgba(0, 0, 0, 1)">.OnAttached();</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">protected</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">override</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">void</code> <code style="color: rgba(0, 0, 0, 1)">OnDetaching()</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">AssociatedObject.LayoutUpdated -= AssociatedObject_LayoutUpdated;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">base</code><code style="color: rgba(0, 0, 0, 1)">.OnDetaching();</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">void</code> <code style="color: rgba(0, 0, 0, 1)">AssociatedObject_LayoutUpdated(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">sender, EventArgs e)</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">BindingExpression binding = AssociatedObject.GetBindingExpression(RadioButton.IsCheckedProperty);</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">if</code> <code style="color: rgba(0, 0, 0, 1)">(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">null</code> <code style="color: rgba(0, 0, 0, 1)">!= binding)</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">binding.UpdateSource();</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></div>
</div>
<br>
XAML:<br>
<br>
<div class="reCodeBlock" style="border: 1px solid rgba(127, 157, 185, 1); border-image: none">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">RadioButton</code> <code style="color: rgba(128, 128, 128, 1)">IsChecked</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"{Binding Value}"</code>&nbsp; <code style="color: rgba(128, 128, 128, 1)">Command</code><code style="color: rgba(0, 0, 0, 1)">=</code><code style="color: rgba(0, 0, 255, 1)">"{Binding ChangeValueCommand}"</code><code style="color: rgba(0, 0, 0, 1)">&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">i:Interaction.Behaviors</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">behaviors:VirtualizedRadioButtonBehavior</code><code style="color: rgba(0, 0, 0, 1)">/&gt;</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">i:Interaction.Behaviors</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 0, 0, 1)">&lt;/</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">RadioButton</code><code style="color: rgba(0, 0, 0, 1)">&gt;</code></span></div>
</div>
<br>
<br>
<br>
I also tried a version where, instead of evaluating the binding, I had a property to compare the bound value to the actual IsChecked value:<br>
<br>
<div class="reCodeBlock" style="border: 1px solid rgba(127, 157, 185, 1); border-image: none">
<div style="background-color: rgba(255, 255, 255, 1)"><span style="margin-left: 0 !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">class</code> <code style="color: rgba(0, 0, 0, 1)">VirtualizedRadioButtonBehavior : Behavior&lt;RadioButton&gt;</code></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 0, 0, 1)">DependencyProperty SynchronizedPropertyProperty = DependencyProperty.Register(</code><code style="color: rgba(0, 0, 255, 1)">"SynchronizedProperty"</code><code style="color: rgba(0, 0, 0, 1)">, </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">typeof</code><code style="color: rgba(0, 0, 0, 1)">(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">bool</code><code style="color: rgba(0, 0, 0, 1)">?), </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">typeof</code><code style="color: rgba(0, 0, 0, 1)">(VirtualizedRadioButtonBehavior), </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">new</code> <code style="color: rgba(0, 0, 0, 1)">PropertyMetadata(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">null</code><code style="color: rgba(0, 0, 0, 1)">));</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">public</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">bool</code><code style="color: rgba(0, 0, 0, 1)">? SynchronizedProperty</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">get</code> <code style="color: rgba(0, 0, 0, 1)">{ </code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">return</code> <code style="color: rgba(0, 0, 0, 1)">(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">bool</code><code style="color: rgba(0, 0, 0, 1)">?)GetValue(SynchronizedPropertyProperty); }</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">set</code> <code style="color: rgba(0, 0, 0, 1)">{ SetValue(SynchronizedPropertyProperty, value); }</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">protected</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">override</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">void</code> <code style="color: rgba(0, 0, 0, 1)">OnAttached()</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">AssociatedObject.LayoutUpdated += AssociatedObject_LayoutUpdated;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">base</code><code style="color: rgba(0, 0, 0, 1)">.OnAttached();</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">protected</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">override</code> <code style="color: rgba(0, 102, 153, 1); font-weight: bold">void</code> <code style="color: rgba(0, 0, 0, 1)">OnDetaching()</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">AssociatedObject.LayoutUpdated -= AssociatedObject_LayoutUpdated;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">base</code><code style="color: rgba(0, 0, 0, 1)">.OnDetaching();</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span style="margin-left: 0 !important">&nbsp;</span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">void</code> <code style="color: rgba(0, 0, 0, 1)">AssociatedObject_LayoutUpdated(</code><code style="color: rgba(0, 102, 153, 1); font-weight: bold">object</code> <code style="color: rgba(0, 0, 0, 1)">sender, EventArgs e)</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 102, 153, 1); font-weight: bold">if</code> <code style="color: rgba(0, 0, 0, 1)">(SynchronizedProperty != AssociatedObject.IsChecked)</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">{</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 48px !important"><code style="color: rgba(0, 0, 0, 1)">AssociatedObject.IsChecked = SynchronizedProperty;</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 36px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(255, 255, 255, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 24px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
<div style="background-color: rgba(248, 248, 248, 1)"><span><code>&nbsp;&nbsp;&nbsp;&nbsp;</code><span style="margin-left: 12px !important"><code style="color: rgba(0, 0, 0, 1)">}</code></span></span></div>
</div>
<br>
<br>
I am not sure if it's any faster, but I settled for refreshing the binding, because the usage was simpler.<br></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-3138410" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="3649873" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="3649873"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="3649873"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <a class="username e2e-username" href="/forums/profile/a8983b68-35c4-41cd-a696-d92d0f07a92a">Tim</a>
                                                    
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1437180119037"><span class="u-dib">18 Jul 2015,&nbsp;</span><span class="u-dib">12:41 AM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#3649873"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-3649873">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text"><p>Hi Telerik,</p>
<p>&nbsp;A customer of ours is having this issue with the grid. &nbsp;When the grid first displays all is well. &nbsp;When they scroll down and then scroll back up to the top, the text in one of the columns changes to different values. &nbsp;Unfortunately it is something that we have been unable to replicate in house.</p>
<p>&nbsp;Reviewing our xaml, we note that t<span style="line-height: 1.5">he GridViewDataColumn columns </span><span style="line-height: 1.5">that</span><span style="line-height: 1.5"> are teh problematic are ones where we have a custom CellTemplate defined. &nbsp;</span></p>
<p>Researching your forum I came across this link:&nbsp;<a href="http://www.telerik.com/forums/difference-between-cellstyle-template-and-celltemplate" rel="ugc">http://www.telerik.com/forums/difference-between-cellstyle-template-and-celltemplate</a></p>
<p>I have now reworked the xaml to use CellStyle instead of CellTemplate.</p>
<p>In house everything works as is and I am hopeful to supply this change to our customer to have them try it.</p>
<p>In trying to understand if this will help and if so why I used JustDecompile on the Telerik.Windows.Control.GridView.dll&nbsp;and note that in&nbsp;Telerik.Windows.Control.GridView.DataCellsPresenter.SyncProperties() method there is a&nbsp;NotifyPropertyChanged call for CellStyle only. &nbsp;there is no call for CellTemplate.</p>
<p>Should Telerik&nbsp;also have a NotifyPropertyChanged call to CellTemplate in ​this&nbsp;SyncProperties() method and until it is added&nbsp;should we use CellStyle in our Xaml to assure everything stays synced when Row Virtualization is used?</p>
<p>&nbsp;-&nbsp;<span style="line-height: 1.5">Tim</span></p>
<p><span style="line-height: 1.5">&nbsp;</span></p>
<p>&nbsp;​</p>
<p>&nbsp;</p></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-3649873" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>
                        <div id="3652619" class="row u-mb35 no-gutters answer-separator e2e-thread-message d-block d-lg-flex">
                            <div class="score-col d-flex d-lg-block u-pr e2e-msg-votes-wrapper">
                                <div class="vote-touch mb-2 e2e-msg-vote-up-wrapper">
                                    <div class="vote up e2e-msg-vote-up" data-id="3652619"></div>
                                </div>

                                <div class="answer-score text-light e2e-msg-votes">0</div>

                                <div class="vote-touch vote-touch-down mt-2 e2e-msg-vote-down-wrapper">
                                    <div class="vote down e2e-msg-vote-down" data-id="3652619"></div>
                                </div>

                                <div class="u-mt10 u-tac u-mob-mt0 u-mob-ml10">
                                    
                                    
                                </div>
                            </div>
                            <div class="col-lg answer-container u-mob-w100">
                                <div class="edit-post-popup">
                                    <div class="row no-gutters justify-content-between u-mb10 text-light align-items-start align-content-lg-center">
                                        <div class="col-9 col-sm-10 col-lg-10 d-block d-lg-flex messageby-col">
                                            <div class="achievements-tooltip-zone d-inline d-lg-flex messageby-col e2e-msg-author">
                                                <div class="u-dib"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                                                <div class="u-dib achievements-tooltip-anchor">
                                                    <span class="username e2e-username support-officer-badge">Dimitrina</span>
                                                    <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                                                </div>
                                            </div>
                                            <div class="modified d-inline d-lg-block e2e-msg-action">
                                                answered on <span class="local-datetime e2e-th-date" data-timestamp="1437488267567"><span class="u-dib">21 Jul 2015,&nbsp;</span><span class="u-dib">02:17 PM</span></span>
                                            </div>
                                        </div>
                                        <div class="col-auto actions-container">
                                            
                                            <a href="#"
                                               class="social-care e2e-msg-care"
                                               data-url="https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems#3652619"
                                               data-title="Share this answer"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="i-care">
    <path d="M15,13.5a2.5,2.5,0,0,1-5,0,2.62,2.62,0,0,1,.11-.69L5,10a2.42,2.42,0,0,1-1.49.51,2.5,2.5,0,0,1,0-5,2.42,2.42,0,0,1,1.61.61l5-2.78A2.54,2.54,0,0,1,10,2.5,2.5,2.5,0,1,1,12.5,5a2.46,2.46,0,0,1-1.83-.81L5.74,6.9A2.54,2.54,0,0,1,6,8a2.5,2.5,0,0,1-.33,1.22l4.9,2.7A2.49,2.49,0,0,1,15,13.5Z" />
</svg></a>
                                        </div>
                                    </div>
                                    <div id="msg-content-3652619">
                                        <div>
                                            
                                            <div class="pb-3 u-mr20 msg-content e2e-msg-text">Hi,<br>
<br>
Would you please share how have you defined the hyperlink columns? Generally such issues may be observed when working with the visual elements (i.e. GridViewCell).&nbsp;You can also refer to the documentation on&nbsp;<a href="http://docs.telerik.com/devtools/silverlight/controls/radgridview/troubleshooting/style-disappears-scrolling.html#styling-or-content-mixed-up-on-scrolling" style="margin-left: -25px; padding-left: 25px" target="blank" rel="ugc">Styling or content mixed-up on scrolling</a>.<br>
<br>
A way to diagnose if this is the reason would be to disable RadGridView's UI virtualization.&nbsp;Please take a look at this&nbsp;<a href="http://docs.telerik.com/devtools/silverlight/controls/radgridview/features/ui-virtualization.html" target="_blank" rel="ugc">article for a reference on UI Virtualization</a>.&nbsp;<br>
<br>
How does&nbsp;<a href="http://docs.telerik.com/devtools/silverlight/controls/radgridview/columns/columntypes/column-types-hyperlink-column.html#hyperlink-column" style="margin-left: -25px; padding-left: 25px" target="blank" rel="ugc">Hyperlink Column</a>&nbsp;or&nbsp;<a href="http://docs.telerik.com/devtools/silverlight/controls/radgridview/columns/columntypes/column-types-dynamic-hyperlink-column#dynamic-hyperlink-column" style="margin-left: -25px; padding-left: 25px" target="blank" rel="ugc">Dynamic Hyperlink Column</a>&nbsp;work for you?<br>
<br>
Regards,<br>
 Dimitrina <br>
Telerik
<div class="forumBaloon">
Do you want to have your say when we set our development plans?
Do you want to know when a feature you care about is added or when a bug fixed?
Explore the <a target="_blank" href="http://www.telerik.com/support/feedback" rel="ugc">
Telerik Feedback Portal</a>
and vote to affect the priority of the items
</div></div>
                                        </div>
                                        
                                        <div class="loader-container centered" style="display: none">
                                            <div class="loader loader-med"></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="u-mt10 e2e-answer-comments">
                                    
<div id="comments-3652619" class="u-pr">
    
    <div class="loader-container" style="display:none"></div>
</div>
                                </div>
                            </div>
                        </div>

                    <div id="answers-list-loader" class="loader-container centered" style="display: none">
                        <div class="loader"></div>
                    </div>
                </div>

                
            </div>
        </div>

        <div class="col-side-bar list-side-nav thread-sidebar">
            <div class="u-pl15 u-pt30">
                <div class="mb-5">
                    <div class="side-nav-heading u-pb20">Tags</div>
                        <span class="tag selected mr-1 mb-1 e2e-thread-tag" title="GridView">
                            <span class="e2e-tag-name">GridView</span>
                        </span>
                </div>

                <div class="side-nav-heading u-pb20 e2e-thread-asked-by-title">Asked by</div>
                <div class="e2e-thread-asked-by achievements-tooltip-zone d-flex align-items-center">
                    <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                    <div class="u-dib achievements-tooltip-anchor">
                        <a class="username e2e-username" href="/forums/profile/8d76c6c5-83bf-4f50-8095-54150a65b25b">Eugen Rata</a>
                        
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                    </div>
                </div>

                <div class="mt-5">
                    <div class="side-nav-heading u-pb20 e2e-thread-answers-by-title">Answers by</div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/support-officer.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <span class="username e2e-username">Milan</span>
                                <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <a class="username e2e-username" href="/forums/profile/adaf1806-7277-4ca0-8b3b-f7416014df92">Pedro</a>
                                
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/support-officer.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" onerror="this.src =&#x27;/forums/images/avatarimages/default.gif&#x27;;this.onerror = null" src="/forums/images/adminimages/vladimir.enchev@telerik.com.jpg" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <span class="username e2e-username">Vlad</span>
                                <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <a class="username e2e-username" href="/forums/profile/b5ab188d-3e35-4eca-91a4-16b19175ed05">Rupendra</a>
                                
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <a class="username e2e-username" href="/forums/profile/f45bc240-33d0-4b7c-afde-e575f633ea81">Ed</a>
                                
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <a class="username e2e-username" href="/forums/profile/741898a1-5f9d-425b-8704-50a432c176d6">Calvin</a>
                                
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <a class="username e2e-username" href="/forums/profile/d5934430-e1a7-4c53-aefd-0efe8e1439a4">Mikle</a>
                                
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <a class="username e2e-username" href="/forums/profile/53fd9040-d006-4bd1-9859-abbe1ee7e00f">Autolog</a>
                                
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/sm-rank-01.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <a class="username e2e-username" href="/forums/profile/a8983b68-35c4-41cd-a696-d92d0f07a92a">Tim</a>
                                
<div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Top achievements</span>
    <div class="row no-gutters d-flex justify-content-between">
            <div class="col-md-6 u-tac u-mt10 e2e-ach-rank">
                <img src="/forums/images/forum-gamification/rank-01.svg" 
                     loading="lazy" width="56" height="56" class="e2e-ach-icon" />
                <span class="achievement-name u-db e2e-ach-name">Rank 1</span>
            </div>

    </div>
</div>
                            </div>
                        </div>
                        <div class="u-mb10 e2e-thread-answers-by achievements-tooltip-zone d-flex align-items-center">
                            <div class="u-mr13 u-dib avatar-rank" style="--rank-src: url(&#x27;../images/forum-gamification/support-officer.svg&#x27;)"><img alt="" class="user-avatar e2e-avatar" loading="lazy" src="/forums/images/avatarimages/default.gif" /></div>
                            <div class="u-dib achievements-tooltip-anchor">
                                <span class="username e2e-username">Dimitrina</span>
                                <div class="achievements-tooltip-container e2e-ach-tooltip">
    <span class="achievements-title e2e-ach-title">Telerik team</span>
    <div class="row no-gutters d-flex justify-content-between">
        <div class="col-md-12 u-tac u-mt10 e2e-ach-support">
            <img src="/forums/images/forum-gamification/support-officer.svg" loading="lazy" width="56" height="56" class="e2e-ach-icon" />
        </div>
    </div>
</div>
                            </div>
                        </div>
                </div>
            </div>
        </div>
    </div>
    <div class="edit-overlay" style="display: none">
    </div>
</div></th:partial>
</div>

<div id="social-care-box" class="e2e-care-box">
    <div class="arrow"></div>
    <div class="content">
        <div class="title u-mb20 e2e-care-title">Share this question</div>
        <div class="u-mb35">
            <ul class="social-network-list">
                <li><a href="#" data-url="https://www.facebook.com/sharer.php?u={url}" class="e2e-care-fb"><svg x="0px" y="0px" width="512px" height="512px" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" class="i-facebook">
    <path d="M290,32c-59.8,0-96,32-96,96v64l-66,0v96l66,0v192h96V288h80l14-96l-94,0v-32c0-32,32-32,32-32h62V34.9C376.8,34,318.6,32,290,32L290,32z" />
</svg></a></li>
                <li><a href="#" data-url="https://twitter.com/share?url={url}" class="e2e-care-tw"><svg x="0px" y="0px" width="512px" height="512px" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" class="i-twitter">
    <path d="M342,64c-50.8,0-91.9,41.2-91.9,91.9c0,7.2,0.8,14.2,2.4,21c-76.4-3.8-144.1-40.4-189.4-96c-7.9,13.6-12.4,29.3-12.4,46.2
	c0,31.9,16.2,60,40.9,76.5c-15.1-0.5-29.2-4.6-41.6-11.5v1.2c0,44.5,31.7,81.7,73.7,90.1c-7.7,2.1-15.8,3.3-24.2,3.3
	c-5.9,0-11.7-0.6-17.3-1.6c11.7,36.5,45.6,63.1,85.9,63.8c-31.7,24.5-71.3,39.2-114.3,39.2c-7.4,0-14.8-0.4-22-1.3
	c40.7,26,89,41.3,140.9,41.3c169.1,0,261.5-140.1,261.5-261.5c0-4-0.1-8-0.2-11.9c18-12.9,33.5-29.1,45.9-47.6
	c-16.5,7.3-34.2,12.3-52.8,14.5c19-11.4,33.6-29.4,40.4-50.8c-17.8,10.5-37.4,18.2-58.4,22.3C392.3,75.1,368.4,64,342,64z" />
</svg></a></li>
                <li><a href="#" data-url="https://www.linkedin.com/shareArticle?url={url}" class="e2e-care-li"><svg x="0px" y="0px" width="512px" height="512px" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" class="i-linkedin">
    <path d="M112,32c-26.5,0-48,21.5-48,48s21.5,48,48,48s48-21.5,48-48S138.5,32,112,32z M64,160v288h96V160H64z M192,160v288h96V288c0-32,32-32,32-32s32,0,32,32v160h96V290.9c0-66.5-13.6-130.9-96-130.9c-36.2,0-62.9,32-64,44.9V160L192,160z" />
</svg></a></li>
                <li><a href="#" data-url="https://reddit.com/submit?url={url}" class="e2e-care-re"><svg x="0px" y="0px" width="512px" height="512px" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" class="i-reddit">
    <path d="M420.3,33c-7,0-14.5,1-22.4,3h-1.7c-12.4,4.8-21.9,12.3-28.8,22.5c-17-7-34-10.4-50.7-10.4c-6.3,0-12.6,0.6-19.1,1.9H296
	c-8.8,2.1-16.5,5.8-23.3,11s-12.4,11.6-16.6,19.1c-5.3,8.7-8.9,31.3-10.5,41.1c-1.7,9.8-2.6,25-2.6,34.7
	c-20.9,1.5-41.8,4.5-62.8,9.1s-40.6,11.9-59,21.9c-1.3,0.4-2.5,0.9-3.5,1.3s-2,0.9-2.9,1.3c-6.2-4.5-13-8-20.5-10.6
	c-7.8-2.6-16.1-3.9-24.9-3.9h-5.8c-8.7,0-16.7,1.6-24.1,4.8s-14.1,7.7-20.3,13.4c-5.8,5.8-10.3,12.2-13.9,19.4
	C1.7,219.9,0,227.4,0,235.3c0.4,10.8,4.4,21.3,11.8,31.4c5.7,8.3,13.8,15.4,24.3,21.1c-0.5,2.1-0.7,4.4-1,6.8
	c-0.2,2.5-0.3,4.8-0.3,6.9c0,10,1.5,20,4.5,30.1c3,10.1,7.4,19.4,13.1,28.1c10.9,16.6,24.5,30.5,40.9,41.6
	c16.4,11,33.8,20.2,52.1,27.2c17.5,6.6,35.5,11.6,54,14.8c18.6,3.3,37.4,5,56.6,5c12.5,0,25.1-0.8,37.5-2.4
	c12.5-1.6,25-3.7,37.6-6.3c23.2-5.5,45.5-13.9,66.8-25.1s39.4-26,54.3-44.3c17.1-20.5,25.6-43.4,25.6-68.8c0-2.6-0.1-5.1-0.4-7.5
	c-0.3-2.4-0.5-4.7-0.9-6.8c10-4.9,18.3-11.9,24.9-21.1c7.1-9.6,10.6-20.3,10.6-32v-3c-1.2-13.4-6.8-25.1-16.3-34.9
	c-9.8-10-21.2-16.7-34.2-20.1h-0.6c-6-1.3-11.6-1.9-16.9-1.9c-14.1-0.2-26.6,3.2-37.4,10.2c-2.3,1.1-5.2,2.8-8.6,5.4
	c-0.8-0.9-1.8-1.3-2.6-1.3l-0.7-0.6c-18.2-9.6-37.5-16.9-57.7-21.8c-20.1-4.9-40.6-8-61.6-9.3c0-7.7,0.7-34.2,1.8-41.9
	s3.7-14.8,7.5-21.4c4.9-9.6,13.4-15.1,25.6-16.4h5.8c7.4,0,14.7,1.1,21.7,3c7.1,2,14.1,4.3,21.2,6.9v1.9c0,7.5,1.5,14.2,4.5,20.3
	c2.9,6,6.9,11.6,11.8,16.5c10.3,10.4,22.8,16.3,37.7,17.5h7.3c14.9,0,28.1-4.8,39.8-14.4c5.3-4.4,9.7-9.6,13.1-15.5s5.5-12.5,6.4-20
	c0.4-1.3,0.6-3.2,0.6-5.8c0.2-11-3.3-21.4-10.3-30.9c-7.1-9.2-15.8-15.7-26.2-19.5h-0.5C436.7,34.3,429.1,32.9,420.3,33L420.3,33z
	 M421.5,60.4c7.2,0.1,13.2,2.7,18.3,7.7C446,73,449,79.2,449,86.7V88c-0.8,6.8-3.9,12.7-9.3,17.6c-5.5,4.9-11.9,7.4-19.1,7.4h-1.9
	c-7.1,0-13.4-2.5-19.4-7.4C393.8,100.9,391,95,391,88v-1.3c0-6.6,2.1-12.1,6.5-16.6c3.8-4.7,8.9-7.7,15.1-8.9c2-0.4,4.4-0.6,7.5-0.6
	C420.5,60.4,421,60.4,421.5,60.4L421.5,60.4z M256.5,186.1c10,0,20.3,0.5,30.8,1.6c10.6,1.1,20.9,2.7,30.8,4.8l9.9,2.6l10.2,2.6
	c17.5,4.9,34.1,11.9,49.9,21.1c15.8,9.2,29,20.8,40,34.9c5.1,7.3,9.2,14.9,12.3,23c3.1,8.1,4.6,16.5,4.6,25.3l0,0v7.6
	c0,2.3-0.4,4.6-1.3,6.7c-2.8,12.4-8.5,24-17.3,34.9c-7.4,10-17,19.2-28.8,27.5c-17.5,11.7-36.4,20.7-56.9,26.9
	c-20.4,6.2-41.3,10.1-62.7,11.8c-3.6,0.5-7.3,0.6-10.8,0.6h-10.8c-21.3,0-42.4-2.2-63.1-6.6c-20.8-4.4-40.3-11.4-58.6-21l-4.5-2.6
	l-4.8-2.2c-13-8.3-24.4-17.5-34.5-27.5c-10.2-11.5-17.2-24-21.1-37.4c-1.7-5.2-2.6-11.2-2.6-18.2c0-18.1,5.6-34.2,16.9-48.3
	c11-14.1,24.4-25.8,40.1-35.2s32.2-16.5,49.7-21.4C200.1,189.9,227.6,186,256.5,186.1L256.5,186.1z M65.7,204h3.2
	c3.2,0,6.1,0.4,8.8,1.3c2.6,0.9,5.4,1.7,8.4,2.6c-8.7,7-16.5,14.6-23.5,22.7c-6.9,8.1-12.8,17-17.7,26.6c-2.8-2-5.2-4.8-7.4-8.6
	c-3-3.5-4.5-7.8-4.5-13.1v-2.1c0.7-7.7,4-14.4,10.3-20.2C50.4,207.9,57.9,204.9,65.7,204L65.7,204z M443.3,203.6
	c6.4,0,12.7,1.5,18.9,4.4c6.1,3.5,10.8,7.8,13.7,13.2c2.1,4.5,3.2,8.6,3.2,12.5c0,5.3-1.2,10.1-3.8,14.4c-2.4,3.6-5,6.7-8,9.2
	c-4.7-10-10.6-19.1-17.6-27.2c-7-8.1-14.9-15.6-23.6-22.7C431.4,204.8,437.1,203.6,443.3,203.6L443.3,203.6z M335.7,246.8
	c-3.6,0-7.4,0.7-11.2,1.9c-6.2,2.2-11.2,5.9-15,11.2c-4,4.7-6.1,10.3-6.1,16.9c0,2.4,0.2,4.2,0.6,5.5v0.6c1.3,7.5,5.1,13.1,11.2,17
	c6.2,4.7,13.2,7,21.1,7c2.5,0,5.5-0.6,9-1.9h0.9c5.6-1.1,11-4.5,16.3-10.2c3.8-5.3,5.8-11.4,5.8-18c0-3-0.6-6.2-2-9.6
	c-1.6-6.2-5.6-11.3-11.8-15.3C348.6,248.6,342.3,246.8,335.7,246.8L335.7,246.8z M176.9,246.7c-2.6,0-4.7,0.2-6.3,0.7
	c-5.8,0.9-10.8,3.1-15.2,6.9c-4.4,3.7-7.4,8.3-9.1,13.6c-0.9,1.2-1.3,2.7-1.3,4.1v4.2c0,7,1.9,13.2,5.8,18.6
	c4.2,5.1,9.6,8.5,16.3,10.2c3,1.2,6.3,1.9,9.9,1.9c8.3,0,15.8-2.8,22.4-8.3c7.1-5.7,10.6-12.8,10.6-21.1v-2c0-7.9-3.3-14.6-9.9-20.1
	C192.9,249.6,185.2,246.7,176.9,246.7L176.9,246.7z M175.3,340.7c-1.2,0-3.2,0.5-5.7,1.3h-0.8c-2.6,0.8-5,2.7-7.3,5.7
	c-1.2,2.1-1.9,4.8-1.9,8c0,2.6,0.6,5.2,1.9,8c1.3,2.2,3.2,3.9,5.8,5.1c24.5,15.4,51.4,23.1,80.7,23.1h4.8c14.1,0,27.8-1.3,41-4
	c13.2-2.7,26.1-6.9,38.5-12.6c1.7-0.9,3.5-1.7,5.4-2.6c1.9-0.8,3.9-1.9,6-3.2c2.2-0.9,4-2.1,5.5-3.8c2.1-2.1,3.3-4.4,3.8-6.8
	c0.4-0.8,0.7-1.9,0.7-3.2c0-1.3-0.4-3.2-1.3-5.8c-1.3-3.2-3.5-5.4-6.4-6.7c-3.3-1.7-6.2-2.6-8.6-2.6c-2.5,0-5.3,0.6-8,2
	c-23.2,13-48.6,19.6-76,19.8c-20.4,0-39.5-3.9-57-11.8c-2.5-0.9-5.7-2.9-9.2-6.1c-0.9-0.4-1.8-0.8-2.8-1.3c-1-0.5-2.2-0.9-3.3-1.3
	C178.4,341.1,176.5,340.6,175.3,340.7L175.3,340.7z" />
</svg></a></li>
            </ul>
        </div>
        <div class="text-separator u-mb35 u-mt10">
            <span>or</span>
        </div>
        <div class="u-mb20">
            <input class="url e2e-care-url" type="text" disabled />
        </div>
        <button class="btn-outline copyBtn e2e-care-copy">Copy link</button>
    </div>
</div>

<script type="application/ld+json">
	{"MainEntity":{"Name":"Virtual mode \u002B custom cell DataTemplate = problems","Headline":"Virtual mode \u002B custom cell DataTemplate = problems","Url":"/forums/virtual-mode-custom-cell-datatemplate-problems","AnswerCount":18,"SuggestedAnswer":[{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1052738","Text":"Hello Eugen Rata,\nThis is a strange problem. Although the grid reuses some of its elements the DataContext for each item is kept in sync and you should not get incorrect values. Could you please send us your project so that we can observe the issue and try to provide a solution.\n\nRegards,\n Milan \nthe Telerik team\n\n\nInstantly find answers to your questions on the new  Telerik Support Portal.\n\nWatch a video on how to optimize your support resource searches and check out more tips on the blogs.\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2010-01-07T09:50:26.677Z","Author":{"Name":"Milan","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1552087","Text":"Hello,\n\nDo you have a solution ? I have the same issue...\nThanks in advance.\n\nBest regards,\nPedro","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-03-07T12:17:52.927Z","Author":{"Name":"Pedro","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1552147","Text":"Hi,\n\u0026nbsp;\nSince this thread was more than a year ago can you post more info about the problem at your end the the grid version?\u0026nbsp;\n\n\nKind regards,\n Vlad \nthe Telerik team\n\n\nRegistration for Q1 2011 What\u2019s New Webinar Week is now open. Mark your calendar for the week starting March 21st and book your seat for a walk through all the exciting stuff we ship with the new release!\n\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-03-07T12:47:56.49Z","Author":{"Name":"Vlad","Image":"vladimir.enchev@telerik.com.jpg","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1612418","Text":"I am having the same issue as the one above. The scenario is described below:\n\nThe grid ItemSource property\u0026nbsp;is getting bound to a structure which is something like given below\n\npublic const string RowDataPropertyName = \u0022RowData\u0022; \nprivate ObservableCollection\u0026lt;DetailsGridRowModel\u0026gt; m_RowData; \npublic ObservableCollection\u0026lt;DetailsGridRowModel\u0026gt; RowData \n{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;get\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;return m_RowData; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;set\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;if (m_RowData == value) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;return; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;m_RowData = value; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;OnNotifyPropertyChanged(RowDataPropertyName); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n}\n\n\nHere each column has a CellTemplate which contains a custom control.\n\n\n\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; . \n\n\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; . \n\n\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; . \n\n\n\nint i = 0; \nforeach (var col in ColumnsCollection) \n{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;GridViewDataColumn column = new GridViewDataColumn(); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;column.CellTemplate = GetDataboundTemplate(i); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;// do something with col here \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;GridView.Columns.Add(column); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;i\u002B\u002B; \n} \n\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; . \n\n\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; . \n\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; . \n\u0026nbsp;\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public DataTemplate GetDataboundTemplate(int columnIndex) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;StringBuilder xaml = new StringBuilder(); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xaml.Append(\u0022\u0026lt;DataTemplate xmlns=\\\u0022 [namespace] \\\u0022 xmlns:my=\\\u0022 [namespace] \\\u0022\u0026gt;\u0022); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xaml.Append(\u0022\u0026lt;my:DetailsGridItemView Context=\\\u0022{Binding ColumnData[\u0022 \u002B columnIndex \u002B \u0022]}\\\u0022 /\u0026gt;\u0022); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xaml.Append(\u0022\u0026lt;/DataTemplate\u0026gt;\u0022); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;DataTemplate template = XamlReader.Load(xaml.ToString()) as DataTemplate; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;return template; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\n\n\nThe DetailsGridItemView control uses the Context property to render itself correctly.\n\nThe correct behavior for the grid is to bind each row\u0026nbsp;to an instance of DetailsGridRowModel. When I\u0026nbsp;disable the row and column virtualization everything works fine.\n\n\nHowever, when I don\u0027t have them set explicitly or I enable them explicitly the followng behavior starts happening.\n\n    The grid starts to re-bind data to a control that is no-longer visible and hence might be re-used. \n    The data that gets picked up for binding is not in the correct order. So the order of items gets lost on sort and that causes a lot of problems and confusion. \n\n\nLet me illustrate. Say\u0026nbsp; the number of rows visible is 5 and the data for each row is the following list. Lets also assume that the == bars represent the top and bottom edges of the grid control.\n\nlet\u0027s say my list is containing the following data\n\n    a\n    b\n    c\n    d\n    e\n    f\n    g\n    h\n    i\n    j\n\nThis is what the user sees then the grid first renders.\n\n\n==================\n\n    a \n    b \n    c \n    d \n    e \n\n==================\n\n    ?\u0026nbsp;\u0026lt;can\u0027t see this right now\u0026gt; \n    ?\u0026nbsp;\u0026lt;can\u0027t see this right now\u0026gt; \n    ?\u0026nbsp;\u0026lt;can\u0027t see this right now\u0026gt; \n    ?\u0026nbsp;\u0026lt;can\u0027t see this right now\u0026gt; \n    ?\u0026nbsp;\u0026lt;can\u0027t see this right now\u0026gt; \n\n\u0026nbsp;\nNow lets assume that the user scolls to the bottom. The user sees the following.\n\n\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\u0026nbsp;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\n\n===================\n\n    f \n    g \n    h \n    i \n    j \n\n===================\n\nHowever now when the user scrolls up, the grid does not pick up the items in the list in the correct order. So this is what the user might see (I say might since what gets picked up and bound doesn\u0027t seem to be deterministic.)\n\n==================\n\n    g \n    i \n    a \n    b \n    d \n\n==================\n\n    ? \u0026lt;can\u0027t see this right now\u0026gt; \n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\u0026nbsp;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\u0026nbsp;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\u0026nbsp;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\u0026nbsp;\n\n\nIf you notice in the illustration above, I have tried to show that the list shown to the user is not fixed at all. It actually changes and depends on various things which change the timing of the the events firing inside such as\n\n    The user stop scrolling and removed the mouse from the scrollbar when he reached at the bottom (as in mousebuttonup event fired or not) and then scrolled up again. \n    OR\u0026nbsp;The user scrolled to the bottom and with mouse button still down scrolled to the top slowly or very quickly, etc. \n\n\u0026nbsp;\nIn fact sometimes if the user now scrolls down this is what he might see which absolutly confuses the user.\n\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\n\n==================\n\n    b \n    d \n\n\n    a\u0026nbsp;\n    c\u0026nbsp;\u0026nbsp; \n    f\n\n==================\u0026nbsp;\u0026nbsp; \n\n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\u0026nbsp; \n    ? \u0026lt;can\u0027t see this right now\u0026gt;\u0026nbsp;\u0026nbsp;\n\n\nIn the real solution I have about 60 rows and 30 are visible on the grid at any time.","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-04-19T20:38:44.993Z","Author":{"Name":"Rupendra","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1618729","Text":"This issue was taken care by the following procedure.\nBinding to the properties was done only in XAML (xaml binding and\u0026nbsp;using converters). Code did not relied on\u0026nbsp;binding the properties to different parts of the control.","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-04-25T19:21:57.763Z","Author":{"Name":"Rupendra","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1711896","Text":"Hi,\n\nI\u0027m currently using version 2010.3.1314.1040.\u0026nbsp;Our gridview typically\u0026nbsp;contains over 1000 rows. One column uses a data template that has a user control, which data binds\u0026nbsp;to a view model.\n\nWith virtualization enabled, we see the behavior described in this thead. The cell value bound changes as you vertically scroll the cell into and out of view. As a former poster describes, the value picked up for binding seems to be re-used or in the wrong order. \n\u0026nbsp;\nI\u0027ve also tried on the 2011.1.419 relase, but see the same behavior.\n\nPlease advise.\u0026nbsp;\n\n\n\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-07T00:49:09.363Z","Author":{"Name":"Ed","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1712007","Text":"Hi,\n\u0026nbsp;Can you post an example where we can reproduce this with our latest official version - Q1 2011 SP1?\nAll the best,\n Vlad \nthe Telerik team\n\n\n\nRegister for the Q2 2011 What\u0027s New Webinar Week. Mark your calendar for the week starting July 18th and\u0026nbsp;book your seat for a walk through of all the exciting stuff we will ship with the new release!\n\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-07T06:42:34.2Z","Author":{"Name":"Vlad","Image":"vladimir.enchev@telerik.com.jpg","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1723527","Text":"At your request we have prepared a test application which illustrates the problem which we are experiencing.\u0026nbsp;\u0026nbsp;\u0026nbsp; \n\nHere is a link to our project files:\u0026nbsp; http://techsupportfromcal.com/VirtualizationScrollingProblem/VirtualizationScrollingProblem.zip\n\nThis is a matter of considerable urgency for us.\u0026nbsp; Thanks for your assistance.\u0026nbsp; \n\nQuoting from the ReadMe file in our test application: \n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;This\u0026nbsp;test\u0026nbsp;application\u0026nbsp;illustrates\u0026nbsp;a\u0026nbsp;problem\u0026nbsp;which\u0026nbsp;we\u0026nbsp;are\u0026nbsp;experiencing\u0026nbsp;with\u0026nbsp;our\u0026nbsp;Telerik\u0026nbsp;Silverlight\u0026nbsp;GridView.\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;The\u0026nbsp;GridView\u0026nbsp;has\u0026nbsp;three\u0026nbsp;columns\u0026nbsp;which\u0026nbsp;display\u0026nbsp;images.\u0026nbsp;The\u0026nbsp;first\u0026nbsp;image\u0026nbsp;column\u0026nbsp;contains\u0026nbsp;a\u0026nbsp;standard\u0026nbsp;Silverlight\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;Image\u0026nbsp;Control.\u0026nbsp;\u0026nbsp;The\u0026nbsp;second\u0026nbsp;column\u0026nbsp;contains\u0026nbsp;a\u0026nbsp;Silverlight\u0026nbsp;User\u0026nbsp;Control\u0026nbsp;which\u0026nbsp;in\u0026nbsp;turn\u0026nbsp;contains\u0026nbsp;a\u0026nbsp;Silverlight\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;Image\u0026nbsp;Control.\u0026nbsp;\u0026nbsp;The\u0026nbsp;third\u0026nbsp;column\u0026nbsp;shows\u0026nbsp;a\u0026nbsp;Silverlight\u0026nbsp;Image\u0026nbsp;Control\u0026nbsp;hosted\u0026nbsp;in\u0026nbsp;a\u0026nbsp;Silverlight\u0026nbsp;Custom\u0026nbsp;Control.\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;As\u0026nbsp;can\u0026nbsp;be\u0026nbsp;seen\u0026nbsp;from\u0026nbsp;running\u0026nbsp;this\u0026nbsp;application,\u0026nbsp;the\u0026nbsp;first\u0026nbsp;two\u0026nbsp;columns\u0026nbsp;display\u0026nbsp;the\u0026nbsp;correct\u0026nbsp;images\u0026nbsp;when\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;scrolling\u0026nbsp;but\u0026nbsp;the\u0026nbsp;third\u0026nbsp;column\u0026nbsp;does\u0026nbsp;not.\u0026nbsp;\u0026nbsp;As\u0026nbsp;you\u0026nbsp;scroll,\u0026nbsp;the\u0026nbsp;images\u0026nbsp;in\u0026nbsp;the\u0026nbsp;third\u0026nbsp;column\u0026nbsp;come\u0026nbsp;from\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;other\u0026nbsp;rows\u0026nbsp;as\u0026nbsp;the\u0026nbsp;Telerik\u0026nbsp;virtualization\u0026nbsp;process\u0026nbsp;reuses\u0026nbsp;some\u0026nbsp;grid\u0026nbsp;components\u0026nbsp;to\u0026nbsp;improve\u0026nbsp;performance.\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;If\u0026nbsp;you\u0026nbsp;set\u0026nbsp;the\u0026nbsp;\u0026nbsp;EnableRowVirtualization\u0026nbsp;property\u0026nbsp;to\u0026nbsp;False,\u0026nbsp;this\u0026nbsp;problem\u0026nbsp;goes\u0026nbsp;away.\u0026nbsp;However,\u0026nbsp;our\u0026nbsp;data\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;sets\u0026nbsp;are\u0026nbsp;often\u0026nbsp;very\u0026nbsp;large\u0026nbsp;and\u0026nbsp;setting\u0026nbsp;this\u0026nbsp;property\u0026nbsp;to\u0026nbsp;False\u0026nbsp;results\u0026nbsp;in\u0026nbsp;an\u0026nbsp;unacceptable\u0026nbsp;degradation\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;in\u0026nbsp;performance.\u0026nbsp;\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;The\u0026nbsp;third\u0026nbsp;image\u0026nbsp;column\u0026nbsp;also\u0026nbsp;contains\u0026nbsp;a\u0026nbsp;textblock\u0026nbsp;which\u0026nbsp;displays\u0026nbsp;the\u0026nbsp;Identifier\u0026nbsp;Name.\u0026nbsp;\u0026nbsp;As\u0026nbsp;can\u0026nbsp;be\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;seen,\u0026nbsp;this\u0026nbsp;value\u0026nbsp;is\u0026nbsp;correct\u0026nbsp;even\u0026nbsp;though\u0026nbsp;the\u0026nbsp;wrong\u0026nbsp;image\u0026nbsp;is\u0026nbsp;usually\u0026nbsp;displayed.\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;We\u0026nbsp;have\u0026nbsp;tried\u0026nbsp;both\u0026nbsp;the\u0026nbsp;User\u0026nbsp;Control\u0026nbsp;and\u0026nbsp;Custom\u0026nbsp;Control\u0026nbsp;approaches\u0026nbsp;in\u0026nbsp;our\u0026nbsp;application\u0026nbsp;and\u0026nbsp;both\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;exhibit\u0026nbsp;this\u0026nbsp;scrolling\u0026nbsp;problem.\u0026nbsp;\u0026nbsp;Of\u0026nbsp;course,\u0026nbsp;our\u0026nbsp;actual\u0026nbsp;controls\u0026nbsp;are\u0026nbsp;much\u0026nbsp;more\u0026nbsp;complex\u0026nbsp;than\u0026nbsp;this\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;sample\u0026nbsp;application.\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;This\u0026nbsp;problem\u0026nbsp;did\u0026nbsp;not\u0026nbsp;occur\u0026nbsp;with\u0026nbsp;the\u0026nbsp;initial\u0026nbsp;release\u0026nbsp;of\u0026nbsp;the\u0026nbsp;Telerik\u0026nbsp;controls\u0026nbsp;from\u0026nbsp;2010\u0026nbsp;Q3.\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;We\u0026nbsp;first\u0026nbsp;noticed\u0026nbsp;this\u0026nbsp;problem\u0026nbsp;after\u0026nbsp;applying\u0026nbsp;SP1\u0026nbsp;to\u0026nbsp;the\u0026nbsp;Q3\u0026nbsp;release.\u0026nbsp;\u0026nbsp;This\u0026nbsp;test\u0026nbsp;application\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;*\u0026nbsp;as\u0026nbsp;requested\u0026nbsp;by\u0026nbsp;Telerik\u0026nbsp;support\u0026nbsp;uses\u0026nbsp;the\u0026nbsp;Q1\u0026nbsp;2011\u0026nbsp;release.\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-15T20:28:25.647Z","Author":{"Name":"Calvin","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1731502","Text":"Could you please advise us regarding any progress in examining this issue. \u0026nbsp; \u0026nbsp;We are actively working on finding a satisfactory work around but so far we have not developed an acceptable solution. \u0026nbsp;\n\nThanks. \u0026nbsp;","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-22T00:59:45.493Z","Author":{"Name":"Calvin","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1731695","Text":"Hi,\n\u0026nbsp;We\u0027ve checked your scenario with the standard Microsoft\u0026nbsp;Silverlight\u0026nbsp;DataGrid and the behavior is exactly the same. It seems that the problem is in your\u0026nbsp;BasicStructure component - please verify this!\nBest wishes,\n Vlad \nthe Telerik team\n\n\n\nRegister for the Q2 2011 What\u0027s New Webinar Week. Mark your calendar for the week starting July 18th and\u0026nbsp;book your seat for a walk through of all the exciting stuff we will ship with the new release!\n\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-22T08:13:11.193Z","Author":{"Name":"Vlad","Image":"vladimir.enchev@telerik.com.jpg","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1733015","Text":"Thanks for the update.\n\n1. Our application uses the Telerik Grid Control, not the Microsoft Grid Control and at least as of this point we are not looking to switch. \n\n2. I would be happy to review any suggestions which you have regarding a possible problem with the BasicStructure component in my test application.\u0026nbsp; However, for purpose of creating this test application I made this component as simple as possible (our actual application is much more complicated).\u0026nbsp; It consists of nothing more than a custom control with two dependency properties and a UI consisting of a textblock and an image control.\u0026nbsp; The textblock refreshes correctly but the image control does not.\u0026nbsp; I don\u0027t mind at all removing the textblock since we don\u0027t actually have one of those in our real application but I can\u0027t remove the image control because that is the whole point of this column in our application. \u0026nbsp;\n\n3.\u0026nbsp; This test application works just fine with your Q3 2010 controls (pre SP1).\u0026nbsp; Here\u0027s a link: \n\u0026nbsp; http://techsupportfromcal.com/VirtualizationScrollingProblem/VirtualizationScrollingProblemQ32010.zip\nIf this test application works just fine with an earlier version of your controls but is broken with the current version of your controls, I would conclude that you must have changed something in how your controls work.\u0026nbsp; That is what we would like you to check into. \u0026nbsp;\n\n4.\u0026nbsp; In our actual application we have two columns which are causing this problem -- one with an image and the other with a list box.\u0026nbsp; It didn\u0027t seem necessary to illustrate both problems since a fix for one of them will most likely provide a solution for both of them.\u0026nbsp; We have tested many different variations of these controls in our application (both Silverlight UserControls and Silverlight Custom Controls) and they all have this same problem.\u0026nbsp;","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-23T02:21:16.35Z","Author":{"Name":"Calvin","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1733442","Text":"Hello,\n\u0026nbsp;Here is how to change your custom control \u002B converter to fix this:\n\n\u0026lt;Style TargetType=\u0022CustomControls:BasicStructure\u0022\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;Setter Property=\u0022Background\u0022 Value=\u0022White\u0022 /\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;Setter Property=\u0022Template\u0022\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;Setter.Value\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;ControlTemplate TargetType=\u0022CustomControls:BasicStructure\u0022\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;Grid x:Name=\u0022LayoutRoot\u0022 Background=\u0022{TemplateBinding Background}\u0022\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;StackPanel Orientation=\u0022Vertical\u0022\u0026gt;\n\u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp;\u0026nbsp;\u0026lt;TextBlock x:Name=\u0022txbImageName\u0022\u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp; \u0026nbsp;\n\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;Text=\u0022{Binding RelativeSource={RelativeSource TemplatedParent},\u0026nbsp; Path=ImageName}\u0022\u0026nbsp;\u0026nbsp;\u0026nbsp; /\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;Image x:Name=\u0022StructureImage\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;Source=\u0022{Binding RelativeSource={RelativeSource TemplatedParent}, \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;Path=ImageName, Converter={StaticResource imageNameToImageConverter}}\u0022\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;Height=\u0022100\u0022 Width=\u0022100\u0022\u0026nbsp; /\u0026gt;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/StackPanel\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/Grid\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/ControlTemplate\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/Setter.Value\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/Setter\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/Style\u0026gt;\n\n\n\npublic class BasicStructureToImageConverter\u0026nbsp; :IValueConverter\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;string imageName = value as string;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;Uri uri = new Uri(@\u0022http://localhost:6449\u0022 \u002B \u0022/images/\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u002B HttpUtility.UrlEncode(imageName) \u002B \u0022.png\u0022, UriKind.Absolute);\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;return new BitmapImage(uri);\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;throw new NotImplementedException();\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\n\nAll the best,\n Vlad \nthe Telerik team\n\n\n\nRegister for the Q2 2011 What\u0027s New Webinar Week. Mark your calendar for the week starting July 18th and\u0026nbsp;book your seat for a walk through of all the exciting stuff we will ship with the new release!\n\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-25T07:37:17.53Z","Author":{"Name":"Vlad","Image":"vladimir.enchev@telerik.com.jpg","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1736879","Text":"Thanks for your response. \u0026nbsp;\n\nI guess that one of the disadvantages of simplifying our test application to remove most of the complexities of our real application is that some of the constraints of our application are no longer clear.\u0026nbsp; Your proposed solution would work nicely in our case if we needed only a simple string in our value converter.\u0026nbsp; In our actual application, however, we need four items of data inside the value converter: \n\n\u0026nbsp;\u0026nbsp; \u0026nbsp;1.\u0026nbsp;\u0026nbsp;\u0026nbsp;a string which via some business logic is converted into the name of the file for our image, \n\n\u0026nbsp;\u0026nbsp; \u0026nbsp;2.\u0026nbsp;\u0026nbsp;\u0026nbsp;a specification of which default image to use if there is no image corresponding to that file name, \n\n\u0026nbsp;\u0026nbsp; \u0026nbsp;3.\u0026nbsp;\u0026nbsp;\u0026nbsp;the height and \n\n\u0026nbsp;\u0026nbsp; \u0026nbsp;4.\u0026nbsp;\u0026nbsp;\u0026nbsp;the width of the desired image.\n\nThat is the reason why our real application and the test application built to simulate the real application, pass in an object which can include each of those four values as properties.","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-07-26T22:20:49.093Z","Author":{"Name":"Calvin","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1757298","Text":"In the absence of a fix for this problem could we just get a confirmation that if we need to pass an object to our value converter, for versions of your RadGridView later than 2010 Q3, there is no simple solution to this virtualization-scrolling problem.\u0026nbsp; \n\nThanks.","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-08-11T03:02:35.36Z","Author":{"Name":"Calvin","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#1777907","Text":"I have a little example of this problem.\nSample application generates some data with selected checkbox in first column.\nRun application. Deselect checkbox in first row. Than scroll down using keyboard. Note selection bar in some rows and wrongly deselected checkboxes.\n\nXAML:\n\n\u0026lt;UserControl x:Class=\u0022GridViewCellTemplateBug.MainPage\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xmlns=\u0022http://schemas.microsoft.com/winfx/2006/xaml/presentation\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xmlns:x=\u0022http://schemas.microsoft.com/winfx/2006/xaml\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xmlns:d=\u0022http://schemas.microsoft.com/expression/blend/2008\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xmlns:mc=\u0022http://schemas.openxmlformats.org/markup-compatibility/2006\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;xmlns:telerik=\u0022http://schemas.telerik.com/2008/xaml/presentation\u0022\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;mc:Ignorable=\u0022d\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;d:DesignHeight=\u0022300\u0022 d:DesignWidth=\u0022400\u0022\u0026gt; \n\u0026nbsp;\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;Grid x:Name=\u0022LayoutRoot\u0022 Background=\u0022White\u0022\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerik:RadGridView x:Name=\u0022rgvProducts\u0022 Grid.Row=\u00221\u0022 Margin=\u00220,10,0,5\u0022 CanUserFreezeColumns=\u0022False\u0022 GridLinesVisibility=\u0022Both\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;HorizontalAlignment=\u0022Stretch\u0022 VerticalAlignment=\u0022Stretch\u0022 FontSize=\u002210\u0022 FontWeight=\u0022Normal\u0022 Height=\u0022Auto\u0022 ShowGroupPanel=\u0022False\u0022\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;IsFilteringAllowed=\u0022True\u0022\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;AutoGenerateColumns=\u0022False\u0022 IsReadOnly=\u0022False\u0022 CanUserSelect=\u0022False\u0022\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerik:RadGridView.Columns\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerik:GridViewDataColumn Header=\u0022Select\u0022 \u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerik:GridViewDataColumn.CellTemplate\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;DataTemplate\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;CheckBox IsChecked=\u0022{Binding Selected}\u0022 IsEnabled=\u0022True\u0022 HorizontalAlignment=\u0022Center\u0022 /\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/DataTemplate\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/telerik:GridViewDataColumn.CellTemplate\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/telerik:GridViewDataColumn\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerik:GridViewDataColumn Header=\u0022Description\u0022 UniqueName=\u0022SKUDescription\u0022 IsReadOnly=\u0022True\u0022 /\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/telerik:RadGridView.Columns\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/telerik:RadGridView\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/Grid\u0026gt; \n\u0026lt;/UserControl\u0026gt; \n\n\nCode:\n\nusing System.Collections.Generic; \nusing System.Windows.Controls; \nusing System.ComponentModel; \n\u0026nbsp;\u0026nbsp;\nnamespace GridViewCellTemplateBug \n{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public partial class MainPage : UserControl \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public MainPage() \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;InitializeComponent(); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;ProductCollection itemList = new ProductCollection(); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;for (int i = 0; i \u0026lt; 100; i\u002B\u002B) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;Product item = new Product(); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;item.Selected = true; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;item.SKUDescription = \u0022Description\u0022 \u002B i.ToString() \u002B \u0022\u0026nbsp;\u0026nbsp; number\u0022 \u002B i.ToString() \u002B i.ToString(); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;itemList.Add(item); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;rgvProducts.ItemsSource = itemList; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public class Product : object, INotifyPropertyChanged \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;private bool _Selected; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public string SKUDescription { get; set; } \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public bool Selected \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;get { return _Selected; } \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;set\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;_Selected = value; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;NotifyPropertyChanged(\u0022Selected\u0022); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public event PropertyChangedEventHandler PropertyChanged; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public void NotifyPropertyChanged(string propertyName) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;if (PropertyChanged != null) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;PropertyChanged(this, new PropertyChangedEventArgs(propertyName)); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public class ProductCollection : List\u0026lt;Product\u0026gt; \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public ProductCollection() : base() { } \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public ProductCollection(Product[] items) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;: base() \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;if (items != null) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;foreach (Product item in items) \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{ \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;this.Add(item); \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;} \n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}; \n} \n\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2011-08-26T09:30:16.043Z","Author":{"Name":"Mikle","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#3138410","Text":"I ran into the same issue with a radiobutton, and short of extending GridViewColumn into my own GridViewRadioButtonColumn, I solved it by creating a behavior which refreshes the binding on the radio buttons\u0026nbsp;manually when the layout updates. It could easily be changed into a behavior for a checkbox:\n\n\npublic class VirtualizedRadioButtonBehavior : Behavior\u0026lt;RadioButton\u0026gt;\n{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;protected override void OnAttached()\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;AssociatedObject.LayoutUpdated \u002B= AssociatedObject_LayoutUpdated;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;base.OnAttached();\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;protected override void OnDetaching()\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;AssociatedObject.LayoutUpdated -= AssociatedObject_LayoutUpdated;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;base.OnDetaching();\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;void AssociatedObject_LayoutUpdated(object sender, EventArgs e)\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;BindingExpression binding = AssociatedObject.GetBindingExpression(RadioButton.IsCheckedProperty);\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;if (null != binding)\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;binding.UpdateSource();\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n}\n\n\nXAML:\n\n\n\u0026lt;RadioButton IsChecked=\u0022{Binding Value}\u0022\u0026nbsp; Command=\u0022{Binding ChangeValueCommand}\u0022\u0026gt;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp; \u0026lt;i:Interaction.Behaviors\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;behaviors:VirtualizedRadioButtonBehavior/\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/i:Interaction.Behaviors\u0026gt;\n\u0026lt;/RadioButton\u0026gt;\n\n\n\n\nI also tried a version where, instead of evaluating the binding, I had a property to compare the bound value to the actual IsChecked value:\n\n\npublic class VirtualizedRadioButtonBehavior : Behavior\u0026lt;RadioButton\u0026gt;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public DependencyProperty SynchronizedPropertyProperty = DependencyProperty.Register(\u0022SynchronizedProperty\u0022, typeof(bool?), typeof(VirtualizedRadioButtonBehavior), new PropertyMetadata(null));\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;public bool? SynchronizedProperty\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;get { return (bool?)GetValue(SynchronizedPropertyProperty); }\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;set { SetValue(SynchronizedPropertyProperty, value); }\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;protected override void OnAttached()\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;AssociatedObject.LayoutUpdated \u002B= AssociatedObject_LayoutUpdated;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;base.OnAttached();\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;protected override void OnDetaching()\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;AssociatedObject.LayoutUpdated -= AssociatedObject_LayoutUpdated;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;base.OnDetaching();\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;void AssociatedObject_LayoutUpdated(object sender, EventArgs e)\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;if (SynchronizedProperty != AssociatedObject.IsChecked)\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;{\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;AssociatedObject.IsChecked = SynchronizedProperty;\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;}\n\n\n\nI am not sure if it\u0027s any faster, but I settled for refreshing the binding, because the usage was simpler.","UpvoteCount":0,"CommentCount":0,"DateCreated":"2014-06-03T13:22:54.347Z","Author":{"Name":"Autolog","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#3649873","Text":"Hi Telerik,\n\u0026nbsp;A customer of ours is having this issue with the grid. \u0026nbsp;When the grid first displays all is well. \u0026nbsp;When they scroll down and then scroll back up to the top, the text in one of the columns changes to different values. \u0026nbsp;Unfortunately it is something that we have been unable to replicate in house.\n\u0026nbsp;Reviewing our xaml, we note that the GridViewDataColumn columns that are teh problematic are ones where we have a custom CellTemplate defined. \u0026nbsp;\nResearching your forum I came across this link:\u0026nbsp;http://www.telerik.com/forums/difference-between-cellstyle-template-and-celltemplate\nI have now reworked the xaml to use CellStyle instead of CellTemplate.\nIn house everything works as is and I am hopeful to supply this change to our customer to have them try it.\nIn trying to understand if this will help and if so why I used JustDecompile on the Telerik.Windows.Control.GridView.dll\u0026nbsp;and note that in\u0026nbsp;Telerik.Windows.Control.GridView.DataCellsPresenter.SyncProperties() method there is a\u0026nbsp;NotifyPropertyChanged call for CellStyle only. \u0026nbsp;there is no call for CellTemplate.\nShould Telerik\u0026nbsp;also have a NotifyPropertyChanged call to CellTemplate in \u200Bthis\u0026nbsp;SyncProperties() method and until it is added\u0026nbsp;should we use CellStyle in our Xaml to assure everything stays synced when Row Virtualization is used?\n\u0026nbsp;-\u0026nbsp;Tim\n\u0026nbsp;\n\u0026nbsp;\u200B\n\u0026nbsp;","UpvoteCount":0,"CommentCount":0,"DateCreated":"2015-07-18T00:41:59.037Z","Author":{"Name":"Tim","Image":"","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"},{"Url":"/forums/virtual-mode-custom-cell-datatemplate-problems#3652619","Text":"Hi,\n\nWould you please share how have you defined the hyperlink columns? Generally such issues may be observed when working with the visual elements (i.e. GridViewCell).\u0026nbsp;You can also refer to the documentation on\u0026nbsp;Styling or content mixed-up on scrolling.\n\nA way to diagnose if this is the reason would be to disable RadGridView\u0027s UI virtualization.\u0026nbsp;Please take a look at this\u0026nbsp;article for a reference on UI Virtualization.\u0026nbsp;\n\nHow does\u0026nbsp;Hyperlink Column\u0026nbsp;or\u0026nbsp;Dynamic Hyperlink Column\u0026nbsp;work for you?\n\nRegards,\n Dimitrina \nTelerik\n\nDo you want to have your say when we set our development plans?\nDo you want to know when a feature you care about is added or when a bug fixed?\nExplore the \nTelerik Feedback Portal\nand vote to affect the priority of the items\n","UpvoteCount":0,"CommentCount":0,"DateCreated":"2015-07-21T14:17:47.567Z","Author":{"Name":"Dimitrina","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Answer"}],"Text":"I have such a code for the grid I\u0027m using                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerik:GridViewDataColumn\u0026nbsp;Header=\u0022Type\u0022\u0026nbsp;DataMemberBinding=\u0022{Binding\u0026nbsp;TypeCombo}\u0022\u0026gt;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerik:GridViewDataColumn.CellTemplate\u0026gt;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;DataTemplate\u0026gt;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;telerikInput:RadComboBox\u0026nbsp;ItemsSource=\u0022{Binding\u0026nbsp;TypeCombo.ItemsSource}\u0022\u0026nbsp;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;SelectedIndex=\u0022{Binding\u0026nbsp;TypeCombo.SelectedIndex,\u0026nbsp;Mode=TwoWay}\u0022\u0026nbsp;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;IsEnabled=\u0022{Binding\u0026nbsp;IsComboTypeEnabled}\u0022/\u0026gt;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/DataTemplate\u0026gt;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/telerik:GridViewDataColumn.CellTemplate\u0026gt;\u0026nbsp;                            \u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026nbsp;\u0026lt;/telerik:GridViewDataColumn\u0026gt;\u0026nbsp;                            \u0026nbsp;            when\u0026nbsp;EnableRowVirtualization is set to true (which is by default) that creates a lots of issues.When scrolling the grid, up \u0026amp; down, cause ComboBoxes are reused, they get filled with wrong values and because of that when TypeCombo.SelectedIndex get\u0027s called I get a lot of \u0022Index out of bounds\u0022 exception. If I set\u0026nbsp;EnableRowVirtualization=false, everything works as expected.\u0026nbsp;There are 15 such columns with custom CellTemplate and DataTemplate.Something must be done here, or at least make by default that\u0026nbsp;EnableRowVirtualization is false, unless you expect that most of people don\u0027t use Lookup comboboxes in their grids, that is very false for most of LOB applications.And by the way, I do have like 40 rows, and when\u0026nbsp;EnableRowVirtualization=true, the scrolling is much slower than virtual mode is set to false.P.S. I\u0027m using latest internal build available as of 1/2/2010.","UpvoteCount":0,"CommentCount":18,"DateCreated":"2010-01-03T00:20:15.163Z","Author":{"Name":"Eugen Rata","@context":"https://schema.org","@type":"Person"},"Comment":[],"@context":"https://schema.org","@type":"Question"},"@context":"https://schema.org","@type":"QAPage","@id":null}
</script>
    </div>
    <link rel="stylesheet" type="text/css" href="https://d6vtbcy3ong79.cloudfront.net/telerik-navigation/3.5.52/css/index-footer.min.css"><footer class="TK-Footer" data-tlrk-nav-version="3.5.52" data-tlrk-nav-template="footer-big-abs-component"><div class="TK-container"><div class="TK-row TK-No-Print"><div class="TK-col-8 TK--Footer-Desktop"><div class="TK-Footer-Featured-Item"><div class="TK-Footer-H">Complete .NET Toolbox</div><a href="https://www.telerik.com/devcraft" class="TK-Footer-Featured-Link">Telerik DevCraft</a></div><div class="TK-Footer-Featured-Item"><div class="TK-Footer-H">Complete JavaScript Toolbox</div><a href="https://www.telerik.com/kendo-ui" class="TK-Footer-Featured-Link">Kendo UI</a></div></div><div class="TK-col-16"><div class="TK-row"><div class="TK-col-6 TK--Footer-Desktop"><div class="TK-Footer-H TK--Footer-Desktop">Get Products</div><ul class="TK-Footer-List"><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/download" class="TK-Footer-Link">Free Trials</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/purchase.aspx" class="TK-Footer-Link">Pricing</a></li></ul></div><div class="TK-col-6 TK--Footer-Desktop"><div class="TK-Footer-H TK--Footer-Desktop">Resources</div><ul class="TK-Footer-List"><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/support/demos" class="TK-Footer-Link">Demos</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/documentation" class="TK-Footer-Link">Documentation</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/support/whats-new/release-history" class="TK-Footer-Link">Release History</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/forums" class="TK-Footer-Link">Forums</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/blogs" class="TK-Footer-Link">Blogs</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/webinars" class="TK-Footer-Link">Webinars</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/videos" class="TK-Footer-Link">Videos</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/services" class="TK-Footer-Link">Professional Services</a></li><li class="TK-Footer-List-Item"><a href="https://www.progress.com/partners/partner-locator?Products&#x3D;KendoUI+and+Telerik" class="TK-Footer-Link">Partners</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/support/virtual-classroom" class="TK-Footer-Link">Virtual Classroom</a></li><li class="TK-Footer-List-Item"><a href="https://www.progress.com/events" class="TK-Footer-Link">Events</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/faqs" class="TK-Footer-Link">FAQs</a></li></ul></div><div class="TK-col-6 TK--Footer-Desktop"><div class="TK-Footer-H TK--Footer-Desktop">Recognition</div><ul class="TK-Footer-List"><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/about/success-stories" class="TK-Footer-Link">Success Stories</a></li><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/about/testimonials" class="TK-Footer-Link">Testimonials</a></li></ul></div><div class="TK-col-6 TK--Footer-Desktop"><div class="TK-Footer-H TK--Footer-Desktop">Get in touch</div><ul class="TK-Footer-List"><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/contact" class="TK-Footer-Link">Contact Us</a></li><li><ul class="TK-Footer-List--inner"><li class="TK-Footer-List-Item"><a href="tel:+18886790442" class="TK-Footer-Phone-Link u-db">USA: <span class="TK-wsn">+1 888 679 0442</span></a></li><li class="TK-Footer-List-Item"><a href="tel:+441344838186" class="TK-Footer-Phone-Link u-db">UK: <span class="TK-wsn">+44 13 4483 8186</span></a></li><li class="TK-Footer-List-Item"><a href="tel:+914069019447" class="TK-Footer-Phone-Link u-db">India: <span class="TK-wsn">+91 406 9019447</span></a></li><li class="TK-Footer-List-Item"><a href="tel:+35928099850" class="TK-Footer-Phone-Link u-db">Bulgaria: <span class="TK-wsn">+359 2 8099850</span></a></li><li class="TK-Footer-List-Item"><a href="tel:+61370688610" class="TK-Footer-Phone-Link u-db">Australia: <span class="TK-wsn">+61 3 7068 8610</span></a></li></ul></li><li><ul class="TK-Footer-List--inner TK-Footer-List-Horizontal TK-Footer-List-Social"><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.facebook.com/telerik" title="Facebook" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path d="M16 7h-1.924C13.461 7 13 7.252 13 7.889V9h3l-.238 3H13v8h-3v-8H8V9h2V7.077C10 5.055 11.064 4 13.461 4H16zM5 0a5 5 0 00-5 5v14a5 5 0 005 5h14a5 5 0 005-5V5a5 5 0 00-5-5z" fill="#000"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">165k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://x.com/telerik" title="X" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 512 512"><path d="M389.2 48h70.6L305.6 224.2 487 464H345L233.7 318.6 106.5 464H35.8L200.7 275.5 26.8 48H172.4L272.9 180.9 389.2 48zM364.4 421.8h39.1L151.1 88h-42L364.4 421.8z" fill="#000"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">50k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.linkedin.com/company/telerik" title="LinkedIn" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path d="M20 19h-3v-5.6c0-3.368-4-3.113-4 0V19h-3V8h3v1.765c1.4-2.586 7-2.777 7 2.476zM6.5 6.732a1.757 1.757 0 01-1.75-1.764A1.757 1.757 0 016.5 3.2a1.758 1.758 0 011.75 1.764A1.757 1.757 0 016.5 6.728zM5 19h3V8H5zM19 0H5a5 5 0 00-5 5v14a5 5 0 005 5h14a5 5 0 005-5V5a5 5 0 00-5-5z" fill="#000" fill-rule="evenodd"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">17k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.twitch.tv/codeitlive" title="Twitch" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 23 24.05"><path d="M1.57.02L0 4.18V20.9h5.75v3.12h3.14l3.13-3.14h4.71L23 14.61V.02zm2.09 2.07h17.25v11.5l-3.66 3.66H11.5l-3.13 3.13v-3.13H3.66zm5.75 10.45h2.09V6.27H9.41zm5.75 0h2.09V6.27h-2.09z" fill="#000"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">4k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.youtube.com/c/telerik" title="YouTube" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="26" height="18.287" viewBox="0 0 26 18.287"><path fill="#010101" d="M25.74 3.945a5.625 5.625 0 0 0-1.034-2.581 3.718 3.718 0 0 0-2.605-1.1c-3.638-.263-9.1-.263-9.1-.263h-.011s-5.458 0-9.1.263a3.719 3.719 0 0 0-2.605 1.1A5.623 5.623 0 0 0 .26 3.945 39.324 39.324 0 0 0 0 8.154v1.972a39.323 39.323 0 0 0 .26 4.208 5.623 5.623 0 0 0 1.033 2.58 4.408 4.408 0 0 0 2.867 1.112c2.08.2 8.84.261 8.84.261s5.463-.008 9.1-.271a3.719 3.719 0 0 0 2.605-1.1 5.625 5.625 0 0 0 1.035-2.582 39.377 39.377 0 0 0 .26-4.208V8.154a39.377 39.377 0 0 0-.26-4.209Zm-15.388 8.6V5.211l6.974 3.665Z"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">14k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://github.com/telerik" title="GitHub" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12,0A12.047,12.047,0,0,0,0,12,12.455,12.455,0,0,0,9.188,24V20.03a2.889,2.889,0,0,1-3.239-1.441c-.273-.46-.756-.959-1.26-.922l-.124-1.4a2.892,2.892,0,0,1,2.593,1.6,1.555,1.555,0,0,0,.9.772,1.89,1.89,0,0,0,1.181-.1,3.3,3.3,0,0,1,.827-1.691h0C6.942,16.382,5.7,14.724,5.2,13.415a5.506,5.506,0,0,1,.855-5.281A.188.188,0,0,0,6.1,7.989a4.6,4.6,0,0,1,.14-3.073,4.858,4.858,0,0,1,2.663,1l.337.2c.141.084.1.036.238.025A10.182,10.182,0,0,1,12,5.792a10.225,10.225,0,0,1,2.553.363l.109.011c-.01,0,.03-.007.1-.046,2.436-1.476,2.349-.993,3-1.206A4.682,4.682,0,0,1,17.9,7.989c-.071.218,2.112,2.217.9,5.426-.494,1.309-1.74,2.968-4.866,3.434h0a3.086,3.086,0,0,1,.879,2.2V24A12.454,12.454,0,0,0,24,12,12.047,12.047,0,0,0,12,0Z"></path></svg></a></li></ul></li></ul></div></div><div class="TK-row TK-row--M2 TK--Footer-Mobile"><div class="TK-col-24"><ul class="TK-Footer-List"><li class="TK-Footer-List-Item"><a href="https://www.telerik.com/contact" class="TK-Footer-Link">Contact Us</a></li><li><ul class="TK-Footer-List--inner TK-Footer-List-Horizontal TK-Footer-List-Social"><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.facebook.com/telerik" title="Facebook" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path d="M16 7h-1.924C13.461 7 13 7.252 13 7.889V9h3l-.238 3H13v8h-3v-8H8V9h2V7.077C10 5.055 11.064 4 13.461 4H16zM5 0a5 5 0 00-5 5v14a5 5 0 005 5h14a5 5 0 005-5V5a5 5 0 00-5-5z" fill="#000"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">165k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://x.com/telerik" title="X" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 512 512"><path d="M389.2 48h70.6L305.6 224.2 487 464H345L233.7 318.6 106.5 464H35.8L200.7 275.5 26.8 48H172.4L272.9 180.9 389.2 48zM364.4 421.8h39.1L151.1 88h-42L364.4 421.8z" fill="#000"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">50k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.linkedin.com/company/telerik" title="LinkedIn" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path d="M20 19h-3v-5.6c0-3.368-4-3.113-4 0V19h-3V8h3v1.765c1.4-2.586 7-2.777 7 2.476zM6.5 6.732a1.757 1.757 0 01-1.75-1.764A1.757 1.757 0 016.5 3.2a1.758 1.758 0 011.75 1.764A1.757 1.757 0 016.5 6.728zM5 19h3V8H5zM19 0H5a5 5 0 00-5 5v14a5 5 0 005 5h14a5 5 0 005-5V5a5 5 0 00-5-5z" fill="#000" fill-rule="evenodd"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">17k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.twitch.tv/codeitlive" title="Twitch" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 23 24.05"><path d="M1.57.02L0 4.18V20.9h5.75v3.12h3.14l3.13-3.14h4.71L23 14.61V.02zm2.09 2.07h17.25v11.5l-3.66 3.66H11.5l-3.13 3.13v-3.13H3.66zm5.75 10.45h2.09V6.27H9.41zm5.75 0h2.09V6.27h-2.09z" fill="#000"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">4k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://www.youtube.com/c/telerik" title="YouTube" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="26" height="18.287" viewBox="0 0 26 18.287"><path fill="#010101" d="M25.74 3.945a5.625 5.625 0 0 0-1.034-2.581 3.718 3.718 0 0 0-2.605-1.1c-3.638-.263-9.1-.263-9.1-.263h-.011s-5.458 0-9.1.263a3.719 3.719 0 0 0-2.605 1.1A5.623 5.623 0 0 0 .26 3.945 39.324 39.324 0 0 0 0 8.154v1.972a39.323 39.323 0 0 0 .26 4.208 5.623 5.623 0 0 0 1.033 2.58 4.408 4.408 0 0 0 2.867 1.112c2.08.2 8.84.261 8.84.261s5.463-.008 9.1-.271a3.719 3.719 0 0 0 2.605-1.1 5.625 5.625 0 0 0 1.035-2.582 39.377 39.377 0 0 0 .26-4.208V8.154a39.377 39.377 0 0 0-.26-4.209Zm-15.388 8.6V5.211l6.974 3.665Z"/></svg> <span class="TK-Footer-Social-Link-Count TK-fs16">14k+</span></a></li><li class="TK-Footer-List-Horizontal-Item"><a href="https://github.com/telerik" title="GitHub" class="TK-Footer-Social-Link"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12,0A12.047,12.047,0,0,0,0,12,12.455,12.455,0,0,0,9.188,24V20.03a2.889,2.889,0,0,1-3.239-1.441c-.273-.46-.756-.959-1.26-.922l-.124-1.4a2.892,2.892,0,0,1,2.593,1.6,1.555,1.555,0,0,0,.9.772,1.89,1.89,0,0,0,1.181-.1,3.3,3.3,0,0,1,.827-1.691h0C6.942,16.382,5.7,14.724,5.2,13.415a5.506,5.506,0,0,1,.855-5.281A.188.188,0,0,0,6.1,7.989a4.6,4.6,0,0,1,.14-3.073,4.858,4.858,0,0,1,2.663,1l.337.2c.141.084.1.036.238.025A10.182,10.182,0,0,1,12,5.792a10.225,10.225,0,0,1,2.553.363l.109.011c-.01,0,.03-.007.1-.046,2.436-1.476,2.349-.993,3-1.206A4.682,4.682,0,0,1,17.9,7.989c-.071.218,2.112,2.217.9,5.426-.494,1.309-1.74,2.968-4.866,3.434h0a3.086,3.086,0,0,1,.879,2.2V24A12.454,12.454,0,0,0,24,12,12.047,12.047,0,0,0,12,0Z"></path></svg></a></li></ul></li></ul></div></div></div></div><div class="TK-row TK-row--M1"><div class="TK-col-24"><a href="https://www.progress.com" aria-label="Go to Progress.com" class="TK-PRGS-Logo-Footer"><svg xmlns="http://www.w3.org/2000/svg" width="130" height="30" viewBox="0 0 512 120"><path fill="#5ce500" d="M95.52 29.33v51a3.93 3.93 0 0 1-1.78 3.08l-1.67 1-12.72 7.35-8.59 5-1.78 1V42.6L21.23 15 43.91 1.93 46 .74a3.94 3.94 0 0 1 3.56 0L81 18.9l14.51 8.38v2.05zM58.36 48.72l-9.79-5.66-22.91-13.23a4 4 0 0 0-3.56 0L1.77 41.57 0 42.6l34.49 19.91v39.83l20.3-11.73 1.79-1a3.94 3.94 0 0 0 1.78-3.08V48.72zM0 82.43l23.86 13.78V68.63z"></path><path fill="#4b4e52" d="M148.09 27.28h-26v70.48h11.55V70.1h14.57c15.77 0 24.45-7.7 24.45-21.69 0-6.35-2.4-21.12-24.55-21.12m12.78 21.31c0 7.95-4.12 11.19-14.24 11.19h-13v-22.1h14.57c8.56 0 12.71 3.57 12.71 10.91M207 46.41l.87.42-2 10.42-1.35-.42a11.32 11.32 0 0 0-3.34-.51c-10.79 0-11.67 8.59-11.67 19v22.44h-10.64V46h10v6.24c2.73-4.2 6-6.37 10.37-6.9a14.55 14.55 0 0 1 7.76 1.07M233.29 45c-8.42 0-15.16 3.2-19.5 9.27-4.56 6.37-5.23 13.85-5.23 17.74 0 16.36 9.7 26.92 24.73 26.92 18.26 0 24.73-14.71 24.73-27.3 0-7.25-2.15-13.82-6-18.51-4.41-5.31-10.87-8.12-18.7-8.12m0 44.38c-8.37 0-13.57-6.66-13.57-17.37s5.2-17.55 13.57-17.55S247 61.23 247 71.78c0 10.83-5.24 17.56-13.66 17.56m114.55-42.93l.87.42-2 10.42-1.35-.42a11.26 11.26 0 0 0-3.33-.51c-10.78 0-11.66 8.59-11.66 19v22.44h-10.66V46h10v6.24c2.73-4.2 6-6.37 10.37-6.9a14.54 14.54 0 0 1 7.73 1.06m38.4 34.76l-.2.57c-2.23 6.36-7.57 7.7-11.65 7.7-8.09 0-13.3-5.37-13.81-14.09h36.59l.13-1a31.26 31.26 0 0 0 .12-4.12v-.93C396.93 54.78 387.48 45 374 45c-7.9 0-14.37 3.1-18.73 9a30.85 30.85 0 0 0-5.54 18c0 16 9.95 26.74 24.74 26.74 11.45 0 19.33-5.82 22.2-16.38l.33-1.2h-10.7zM361 66.05c.9-7.17 5.81-11.73 12.79-11.73 5.33 0 11.64 3.1 12.52 11.73H361zm-60.7-15.71c-3.45-3.58-8.06-5.39-13.76-5.39-15.69 0-22.83 13.81-22.83 26.63 0 13.16 7.06 26.44 22.83 26.44a18.33 18.33 0 0 0 13.35-5.42c0 2.28-.1 4.45-.16 5.38-.58 8.54-4.68 12.51-12.91 12.51-4.47 0-9.61-1.59-10.6-6l-.22-1h-10.54l.17 1.41c1.1 9.12 9.11 14.79 20.9 14.79 10.34 0 17.7-3.9 21.28-11.26 1.73-3.55 2.6-8.72 2.6-15.37V46h-10.13v4.34zm-13.11 38.15c-3.74 0-12.43-1.69-12.43-17.37 0-10.3 4.87-16.7 12.71-16.7 6.06 0 12.52 4.39 12.52 16.7 0 10.87-4.79 17.37-12.81 17.37m159.67-6.31c0 8.23-6.83 16.53-22.09 16.53-13.5 0-21.53-5.85-22.61-16.45l-.15-1.1h10.52l.21.84c1.29 6.38 7.37 7.72 12.24 7.72 5.34 0 11-1.72 11-6.54 0-2.44-1.59-4.18-4.73-5.16-1.86-.55-4.15-1.2-6.56-1.87-4.16-1.16-8.47-2.38-11.12-3.29-6.56-2.35-10.33-6.93-10.33-12.56 0-10.43 10.16-15.11 20.22-15.11 13.46 0 20.42 5.07 21.3 15.49l.09 1.07H434.5l-.14-.82c-1-6-7-6.9-10.48-6.9-3 0-10 .53-10 5.5 0 2.25 1.93 3.91 5.89 5.06 1.18.33 2.94.78 5 1.31 4.22 1.09 9.48 2.46 12.13 3.37 6.59 2.32 9.93 6.67 9.93 13m49.39 0c0 8.23-6.83 16.53-22.09 16.53-13.5 0-21.53-5.85-22.61-16.45l-.11-1.09H462l.12.74c1.29 6.38 7.37 7.72 12.24 7.72 5.34 0 11-1.72 11-6.54 0-2.44-1.59-4.18-4.72-5.16-1.86-.55-4.15-1.2-6.57-1.87-4.16-1.16-8.46-2.38-11.11-3.29-6.57-2.35-10.33-6.93-10.33-12.56 0-10.43 10.16-15.11 20.22-15.11 13.46 0 20.42 5.07 21.29 15.49l.09 1.07H483.9l-.14-.82c-1-6-7-6.9-10.48-6.9-3 0-9.95.53-9.95 5.5 0 2.25 1.93 3.91 5.89 5.06 1.18.33 2.94.78 5 1.31 4.22 1.09 9.48 2.46 12.13 3.37 6.58 2.32 9.93 6.67 9.93 13m8.43-30.78a7.37 7.37 0 1 1 7.29-7.37 7.23 7.23 0 0 1-7.29 7.37m0-13.49a6.12 6.12 0 1 0 6 6.12 5.91 5.91 0 0 0-6-6.12m-.85 7.49v2.46h-2.17v-7.74h3.62a2.58 2.58 0 0 1 2.86 2.7 2.26 2.26 0 0 1-1.49 2.34l1.77 2.7H506l-1.49-2.46h-.68zm1.21-3.49h-1.21v1.73h1.21a.86.86 0 0 0 1-.85.88.88 0 0 0-1-.89"></path></svg></a></div></div><div class="TK-row"><div class="TK-col-12"><p class="TK-Footer-About">Telerik and Kendo UI are part of Progress product portfolio. Progress is the leading provider of application development and digital experience technologies.</p></div><div class="TK-col-24"><div class="TK-row--M3 TK--Footer-Desktop"><ul class="TK-Footer-List-Horizontal"><li class="TK-Footer-List-Horizontal-Item"><a class="TK-Footer-Link TK-Footer-Link-Horizontal" href="https://www.progress.com/company">Company</a></li><li class="TK-Footer-List-Horizontal-Item"><a class="TK-Footer-Link TK-Footer-Link-Horizontal" href="https://www.progress.com/products">Technology</a></li><li class="TK-Footer-List-Horizontal-Item"><a class="TK-Footer-Link TK-Footer-Link-Horizontal" href="https://www.progress.com/company/awards">Awards</a></li><li class="TK-Footer-List-Horizontal-Item"><a class="TK-Footer-Link TK-Footer-Link-Horizontal" href="https://investors.progress.com/press-releases">Press Releases</a></li><li class="TK-Footer-List-Horizontal-Item"><a class="TK-Footer-Link TK-Footer-Link-Horizontal" href="https://www.progress.com/company/press-coverage">Media Coverage</a></li><li class="TK-Footer-List-Horizontal-Item"><a class="TK-Footer-Link TK-Footer-Link-Horizontal" href="https://www.progress.com/company/careers">Careers</a></li><li class="TK-Footer-List-Horizontal-Item"><a class="TK-Footer-Link TK-Footer-Link-Horizontal" href="https://www.progress.com/company/offices">Offices</a></li></ul></div></div></div><div class="TK-row TK-row--M2 TK--Footer-Mobile"><div class="TK-col-24"><ul class="TK-Footer-List"><li class="TK-Footer-List-Item"><a href="https://www.progress.com/company" class="TK-Footer-Link">Company</a></li><li class="TK-Footer-List-Item"><a href="https://www.progress.com/products" class="TK-Footer-Link">Technology</a></li><li class="TK-Footer-List-Item"><a href="https://www.progress.com/company/awards" class="TK-Footer-Link">Awards</a></li><li class="TK-Footer-List-Item"><a href="https://investors.progress.com/press-releases" class="TK-Footer-Link">Press Releases</a></li><li class="TK-Footer-List-Item"><a href="https://www.progress.com/company/press-coverage" class="TK-Footer-Link">Media Coverage</a></li><li class="TK-Footer-List-Item"><a href="https://www.progress.com/company/careers" class="TK-Footer-Link">Careers</a></li><li class="TK-Footer-List-Item"><a href="https://www.progress.com/company/offices" class="TK-Footer-Link">Offices</a></li></ul></div></div><div class="TK-row"><div class="TK-col-16"><p class="TK-Footer-Copy">Copyright &copy; 2024 Progress Software Corporation and/or its subsidiaries or affiliates. All Rights Reserved.</p><p class="TK-Footer-Copy">Progress and certain product names used herein are trademarks or registered trademarks of Progress Software Corporation and/or one of its subsidiaries or affiliates in the U.S. and/or other countries. See <a href="https://www.progress.com/legal/trademarks" class="TK-Footer-Link-Tiny">Trademarks</a> for appropriate markings.</p></div><div class="TK-col-8 TK-tar"><ul class="TK-Footer-List-Horizontal"><li class="TK-Footer-List-Horizontal-Item TK-Footer-List-Horizontal-Item-Effect"><a href="https://www.telerik.com/about/terms-of-use" class="TK-Footer-Link-Tiny">Terms of Use</a></li><li class="TK-Footer-List-Horizontal-Item TK-Footer-List-Horizontal-Item-Effect"><a href="https://www.telerik.com/feedback" class="TK-Footer-Link-Tiny">Site Feedback</a></li><li class="TK-Footer-List-Horizontal-Item TK-Footer-List-Horizontal-Item-Effect"><a href="https://www.progress.com/legal/privacy-center" class="TK-Footer-Link-Tiny" target="_blank" rel="noopener">Privacy Center</a></li><li class="TK-Footer-List-Horizontal-Item TK-Footer-List-Horizontal-Item-Effect"><a href="https://www.progress.com/trust-center" class="TK-Footer-Link-Tiny" target="_blank" rel="noopener">Trust Center</a></li></ul><div class="TLRK-CCPA"><a href="https://forms.progress.com/ccpa-subscription" target="_blank" rel="nofollow noopener">Do Not Sell or Share My Personal Information</a></div><p class="TK-Footer-Power">Powered by <a href="https://www.progress.com/sitefinity-cms" class="TK-Footer-Link-Tiny">Progress Sitefinity</a></p></div></div></div></footer>
</body>
</html>
"""
base_url = (
    "https://www.telerik.com/forums/virtual-mode-custom-cell-datatemplate-problems"
)
