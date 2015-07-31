
    var showSaveToast = function(message) {
        toastr.options.closeButton = false;
        toastr.options.timeOut = 2000;
        toastr.options.fadeOut = 250;
        toastr.options.fadeIn = 250;
        toastr.options.positionClass = 'toast-bottom-right'

        if (message !== undefined) {
            toastr['success'](message + ' saved successful');
        }
        else {
            toastr['success']('Save successful');
        }
    };

    $("#technologyInput").autocomplete({
        source: availableTechnologies
    });

    $('#tags-input').tagsinput({
        allowDuplicates: false,
    });

    var postPlaceholder = 'Create a post for your project it can include images, videos and embeded youtube content.',
        titlePlaceholder = 'Add a title for your new post';

    var LimitedCharEdit = function(element, data, url, placeholder, charCount){
        $(element).editable({
            imageUpload: false,
            imageLink: false,
            buttons: [],
            saveParams: {
                csrfmiddlewaretoken: CSRFToken,
                data: JSON.stringify(data),
                project: projectId,
            },
            saveURL: url,
            autosave: true,
            autosaveInterval: 2500,
            crossDomain: false,
            placeholder: placeholder,
            maxCharacters: charCount,
        }).on('editable.afterSave', function (e, editor, data) {
            showSaveToast();
        });};

    var simpleEdit = function(element, data, url, placeholder){
        $(element).editable({
            imageUpload: false,
            imageLink: false,
            buttons: [],
            saveParams: {
                csrfmiddlewaretoken: CSRFToken,
                data: JSON.stringify(data),
                project: projectId,
            },
            saveURL: url,
            autosave: true,
            autosaveInterval: 2500,
            crossDomain: false,
            placeholder: placeholder
        }).on('editable.afterSave', function (e, editor, data) {
            showSaveToast();
        });};

    var richEdit = function(element, data, url, placeholder){
        $(element).editable({
            inlineMode: false,
            buttons: ['save', 'undo', 'redo', 'removeFormat', 'bold', 'italic', 'underline', 'strikeThrough', 'color', 'fontFamily',
                      'fontSize',  'formatBlock', 'inlineStyle', 'align', 'insertOrderedList',
                      'insertUnorderedList', 'outdent', 'indent', 'createLink', 'insertImage',
                      'insertVideo', 'table', 'insertHorizontalRule' ],
            saveParams: {
                csrfmiddlewaretoken: CSRFToken,
                data: JSON.stringify(data),
                project: projectId,
            },
            saveURL: url,
            autosave: true,
            autosaveInterval: 2500,
            crossDomain: false,
            placeholder: placeholder,
            pasteImage: false,
            pastedImagesUploadURL: imageUploadURL,
            pastedImagesUploadRequestType: 'POST',
            imageMove: true,
            imageUpload: true,
            imageUploadParam: 'file',
            imageUploadURL: imageUploadURL,
            imageUploadParams: {
                csrfmiddlewaretoken: CSRFToken,
                project: projectId,
            },
            imageDeleteConfirmation: true,
            imageDeleteParams: {
                csrfmiddlewaretoken: CSRFToken,
                project: projectId,
            },
            imageDeleteURL: imageDeleteURL,
        })

        // Catch image remove
        .on('editable.afterRemoveImage', function (e, editor, $img) {
            // Set the image source to the image delete params.
            editor.options.imageDeleteParams.src = $img.attr('src');

            // Make the delete request.
            editor.deleteImage($img);
        })

        .on('editable.afterSave', function (e, editor, data) {
            showSaveToast();
        });
    };

    var logoRemoved = function () {
        $("#logo").remove();
        $("#logo-image").append('<img id="logo" class="logo" src=addALogoImage alt="Logo" width="200" style="padding-bottom: 15px;"/>');

        $('.logo').editable({imageUpload: true,
            imageUploadParam: 'file',
            imageUploadURL: imageUploadURL,
            imageUploadParams: {
                logo: true,
                csrfmiddlewaretoken: CSRFToken,
                project: projectId,
            },
            imageButtons: ['replaceImage', 'removeImage'],
            imageDeleteConfirmation: false,
            imageDeleteURL: imageDeleteURL,
            imageDeleteParams: {
                logo: true,
                csrfmiddlewaretoken: CSRFToken,
                project: projectId,
            },
            placeholder: addALogoImage,
            crossDomain: false
        }).on('editable.beforeRemoveImage', function (e, editor, $img) {
            console.log('before');
            // Set the image source to the image delete params.
            editor.options.imageDeleteParams.src = $img.attr('src');

            // Make the delete request.
            editor.deleteImage($img);

            $img.attr.src = editor.options.placeholder;

            logoRemoved();
            $(".logo").on("remove", logoRemoved());
        }).on('editable.afterSave', function (e, editor, data) {
            showSaveToast('Logo');
        });
    };

    $(function(){
        $('.logo').editable({imageUpload: true,
            imageUploadParam: 'file',
            imageUploadURL: imageUploadURL,
            imageUploadParams: {
                logo: true,
                csrfmiddlewaretoken: CSRFToken,
                project: projectId,
            },
            imageButtons: ['replaceImage', 'removeImage'],
            imageDeleteConfirmation: false,
            imageDeleteURL: imageDeleteURL,
            imageDeleteParams: {
                logo: true,
                csrfmiddlewaretoken: CSRFToken,
                project: projectId,
            },
            placeholder: addALogoImage,
            crossDomain: false
        }).on('editable.beforeRemoveImage', function (e, editor, $img) {
            // Set the image source to the image delete params.
            editor.options.imageDeleteParams.src = $img.attr('src');

            // Make the delete request.
            editor.deleteImage($img);

            $img.attr.src = editor.options.placeholder;

            logoRemoved();
        }).on('editable.afterSave', function (e, editor, data) {
            showSaveToast('Logo');
        });
    });

    var addPost = function () {
        $.ajax({
                url: addPostURL,
                type: 'POST',
                dataType: 'json',
                data: {
                        project: projectId,
                        csrfmiddlewaretoken: CSRFToken
                },
                success: function (data, textStatus, xhr) {
                    if (data.status == 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                    else if (data.status === 500) {
                        $('#add-post-errors').removeClass('hidden');
                        $('#add-post-errors-message').html('Internal server error, please try again later.');
                    }
                    else if (data.content.success === true) {
                        $('#add-post-errors').addClass('hidden');

                        $("#time-line").prepend(
                            '<br/>' +
                            '<li class="animated fadeInRight animation-delay-2">' +
                                '<time class="timeline-time" datetime="">' + data.content.date_added + '</time>' +
                                '<i class="timeline-2-point"></i>' +
                                '<div class="panel panel-default">' +
                                    '<div class="panel-heading">' +
                                        '<div id="' + data.content.post_id + '" class="new-post-title-edit" style="color: black;"></div>' +
                                    '</div>' +
                                    '<div id="' + data.content.post_id + '" class="new-post-edit"></div>' +
                                    '<div style="padding: 5px;">' +
                                        '<div style="display: inline-block">' +
                                            '<label>Author </label>' +
                                            '<select id="' + data.content.username + '-user-selection" class="user-selection" selected="' + data.content.username + '" onchange="updatePost(' + data.content.post_id + ', "author", $(this.selectedOptions[0]).val())">' +
                                            '</select>' +
                                        '</div>' +
                                        '<div class="pull-right">' +
                                            '<input type="checkbox" name="' + data.content.post_id + '-is-adimn" onchange="updatePost(' + data.content.post_id + ', &apos;published&apos;, this.checked)">Publish post<br>' +
                                        '</div>' +
                                        '<div id="update-post-errors" class="hidden">' +
                                            '<p style="text-align: center; color: red;">' +
                                                '<i class="fa fa-exclamation-circle" style="color: red;"></i>' +
                                                '<span id="update-post-errors-message"></span>' +
                                            '</p>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                            '</li>'
                        );

                        var authors = $('#' + data.content.username + '-user-selection');
                        $('.creator-name').each(function(){
                            $(authors).append('<option value=' + this.id + '>' + (this.childNodes[1]).text + '</option>')
                        });

                        $('.new-post-title-edit').each(function() {
                            simpleEdit($(this), {'field': 'title', 'post': data.content.post_id}, updatePostURL, titlePlaceholder)
                        });
                        $('.new-post-edit').each(function() {
                            richEdit($(this), {'field': 'post', 'post': data.content.post_id}, updatePostURL, postPlaceholder)
                        });

                        $('.new-post-title-edit').find('.fr-placeholder').each(function() {
                            $(this).css('color', 'black');
                        });
                    }
                    else {
                        $('#add-post-errors').removeClass('hidden');
                        $('#add-post-errors-message').text(data.content.message);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#add-post-errors').removeClass('hidden');
                    $('#add-post-errors-message').text('An error has occurred, we are working to fix it.');
                }
            });
    };

    var updatePost = function (post, field, value) {
        $.ajax({
                url: updatePostURL,
                type: 'POST',
                dataType: 'json',
                data: {data: JSON.stringify({'field': field, 'value': value, 'post':  post}),
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                    if (data.status === 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                    else if (data.status === 500) {
                        $('#update-post-errors').removeClass('hidden');
                        $('#update-post-errors-message').text('Internal server error, please try again later.');
                    }
                    else if (data.content.success === true) {
                        $('#update-post-errors').addClass('hidden');
                        showSaveToast('Post');
                    }
                    else {
                        $('#update-post-errors').removeClass('hidden');
                        $('#update-post-errors-message').text(data.content.message);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#update-post-errors').removeClass('hidden');
                    $('#update-post-errors-message').text('An error has occurred, we are working to fix it.');
                }
            });
    };

    var userLookupKeyup = function () {
        if (event.keyCode == 13) {
            userLookup();
        }
    };

    var userLookup = function (username) {
        var username = $('#creatorInput').val();

        if (username.length > 0) {
            $.ajax({
                url: getUserURL,
                type: 'POST',
                dataType: 'json',
                data: {username: username,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                    if (data.status == 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                    else if (data.status === 500) {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text('Internal server error, please try again later.');
                    }
                    else if (data.success === true) {
                        $('#creator-error').addClass('hidden');

                        var new_creators = $('#add-creator');

                        new_creators.html('<div id="new-creator-div" style="margin-top: 15px;">' +
                                            '<a class="pull-left" href="#">' +
                                                '<img src="' + data.thumbnail + '" alt="' + data.full_name + '" class="img-circle" style="width: 50px">' +
                                            '</a>' +
                                            '<h4 class="media-heading"><a href="#" style="color: white">' + data.full_name + '</a></h4>' +
                                            '<a class="btn btn-default btn-sm" onClick="addCreator(&quot;' + data.username +'&quot;, &quot;' + data.thumbnail + '&quot;, &quot;' + data.full_name + '&quot;)" style="margin-top: 5px">Add Creator</a>' +
                                          '</div>');
                    }
                    else {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text(data.message);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#creator-error').removeClass('hidden');
                    $('#creator-error-message').text('An error has occurred, we are working to fix it.');
                }
            });
        }
        else {
            $('#creator-error').removeClass('hidden');
            $('#creator-error-message').html('Please provide a username');
        }

        $('#creatorInput').val('');
    };

    var getNewCreatorElements = function(username, fullname, thumbnail, parentId) {
         return '<div id="' + parentId + '" class="creator"> \
                     <div class="row"> \
                        <div class="col-md-3"> \
                            <a class="pull-left" href="#"> \
                            <img src="' + thumbnail + '" alt="' + fullname + '" class="img-circle" style="width: 50px; height: 50px;"> \
                            </a> \
                        </div> \
                        <div class="col-md-9" style="text-align: left;"> \
                            <h4 id="' + username + '-heading" class="media-heading creator-name"><a href="#" style="color: white">' + fullname + '</a> \
                            </h4> \
                            <p style="margin-bottom: 0px;"><strong>Awaiting Confirmation</strong></p> \
                            <input type="checkbox" name="is-adimn" style="color: white; onchange="updateCreator(&apos;'+ username +'&apos;, &apos;admin&apos;, this.checked)"">Project administrator<br> \
                        </div> \
                     </div> \
                     <div class="row"> \
                        <div id="creator-' + username + '-summary" class="creator-edit" name="' + username + '" style="margin-bottom: 0px;"></div> \
                     </div> \
                     <hr style="margin: 10px 0px 0px 0px; color: white;"> \
                </div> ';
    }


    var reactivateCreator = function (username, fullname, thumbnail) {
        $.ajax({
                url: updateCreatorURL,
                type: 'POST',
                dataType: 'json',
                data: {username: username,
                       field: 'active',
                       value: true,
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                    if (data.status == 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                    else if (data.status === 500) {
                        $('#prior-creator-error').removeClass('hidden');
                        $('#prior-creator-error-message').text('Internal server error, please try again later.');
                    }
                    else if (data.content.success === true) {
                        $('#prior-creator-error').addClass('hidden');
                        var summary = $('#creator-' + username + '-summary'),
                            creators = $('#creators');

                        creators.append(getNewCreatorElements(username, fullname, thumbnail, 'creator-' + username));
                        var header = $('#' + username + '-heading');
                        header.append('<i id="creator-' + username + '-icon" class="fa fa-minus-circle pull-right" style="color: white; padding-left: 5px;" onclick="removeCreator(&apos;' + username + '&apos;, &apos;' + fullname + '&apos;, &apos;' + thumbnail + '&apos;)"> </i>')

                        var newSummary = creators.find('#creator-' + username + '-summary');
                        newSummary.append(summary);

                        $('#prior-creator-' + username).remove()

                        var priorCreatorsContainer = $('#prior-creators-container'),
                            priorCreators = priorCreatorsContainer.find('.creator');

                        if (priorCreators.length === 0 ){
                            priorCreatorsContainer.addClass('hidden');
                        }

                        showSaveToast('Creator');
                    }
                    else {
                        $('#prior-creator-error').removeClass('hidden');
                        $('#prior-creator-error-message').text(data.content.message);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#prior-creator-error').removeClass('hidden');
                    $('#prior-creator-error-message').text('An error has occurred, we are working to fix it.');
                }
        });
    };

    var updateCreator = function (username, field, value) {
        $.ajax({
                url: updateCreatorURL,
                type: 'POST',
                dataType: 'json',
                data: {username: username,
                       field: field,
                       value: value,
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                    if (data.status == 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                    else if (data.status === 500) {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text('Internal server error, please try again later.');
                    }
                    else if (data.content.success === true) {
                        $('#creator-error').addClass('hidden');
                        showSaveToast('Creator');
                    }
                    else {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text(data.content.message);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#creator-error').removeClass('hidden');
                    $('#creator-error-message').text('An error has occurred, we are working to fix it.');
                }
        });
    };

    var removeCreator = function (username, fullname, thumbnail) {
        $.ajax({
                url: removeCreatorURL,
                type: 'POST',
                dataType: 'json',
                data: {username: username,
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                    if (data.status == 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                    else if (data.status === 500) {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text('Internal server error, please try again later.');
                    }
                    else if (data.content.success === true) {
                        $('#prior-creators-container').removeClass('hidden');

                        $('#creator-error').addClass('hidden');
                        var summary = $('#creator-' + username + '-summary'),
                            creators = $('#prior-creators');

                        creators.append(getNewCreatorElements(username, fullname, thumbnail, 'prior-creator-' + username));

                        var newSummary = creators.find('#creator-' + username + '-summary');
                        newSummary.append(summary);

                        $('#creator-' + username).remove();

                        var header = $('#' + username + '-heading');
                        header.append('<i id="creator-' + username + '-icon" class="fa fa-plus-circle pull-right" style="color: white; padding-left: 5px;" onclick="reactivateCreator(&apos;' + username + '&apos;, &apos;' + fullname + '&apos;, &apos;' + thumbnail + '&apos;)"> </i>')

                        showSaveToast('Creator');
                    }
                    else {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text(data.content.message);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#creator-error').removeClass('hidden');
                    $('#creator-error-message').text('An error has occurred, we are working to fix it.');
                }
            });
    };

    var addCreator = function (username, thumbnail, fullName) {
        if (username.length > 0) {
            $.ajax({
                url: addCreatorURL,
                type: 'POST',
                dataType: 'json',
                data: {username: username,
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                    if (data.status == 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                     else if (data.status === 500) {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text('Internal server error, please try again later.');
                    }
                    else if (data.content.success === true) {
                        $('#creator-error').addClass('hidden');

                        var creators = $('#creators');

                        creators.append(getNewCreatorElements(username, fullName, thumbnail, 'creator-' + username));

                        var header = $('#' + username + '-heading');
                        header.append('<i id="creator-' + username + '-icon" class="fa fa-minus-circle pull-right" style="color: white; padding-left: 5px;" onclick="removeCreator(&apos;' + username + '&apos;, &apos;' + fullName + '&apos;, &apos;' + thumbnail + '&apos;)"> </i>')

                        $('#new-creator-div').remove();

                        $('#creator-' + username + '-summary').editable({
                            imageUpload: false,
                            imageLink: false,
                            buttons: ['bold', 'italic', 'underline', 'fontSize', 'sep', 'formatBlock',
                                      'blockStyle', 'align',  'outdent', 'indent', 'sep', 'undo', 'redo'],
                            saveParams: {
                                csrfmiddlewaretoken: CSRFToken,
                                field: 'summary',
                                project: projectId,
                                username: username
                            },
                            saveURL: updateCreatorURL,
                            autosave: true,
                            autosaveInterval: 2500,
                            crossDomain: false,
                            placeholder: "Add a description of this creator's contribution"
                        });

                        $('.user-selection').each(function() {
                            $(this).append('<option value='+ username + '>' + fullName + '</option>')
                        })

                        $('.creator-edit').find('.fr-placeholder').each(function() {
                            $(this).css('color', 'white');
                        });

                        showSaveToast('Creator');
                    }
                    else {
                        $('#creator-error').removeClass('hidden');
                        $('#creator-error-message').text(data.content.message);
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#creator-error').removeClass('hidden');
                    $('#creator-error-message').text('An error has occurred, we are working to fix it.');
                }
            });
        }
        else {
            $('#creator-error').removeClass('hidden');
            $('#creator-error-message').text('Please provide a username');
        }

        $('#creatorInput').val('');
        $('#addCreator').addClass('hidden');
    };

    var newTechnology = function () {
        $('#addTechnology').removeClass('hidden');

        if (event.keyCode == 13) {
            addTechnology();
        }
    };

    var addTechnology = function () {
        var raw = $('#technologyInput').val(),
            value = raw.substr(0, 1).toUpperCase() + raw.substr(1);

        $.ajax({
            url: addTechnologyURL,
            type: 'POST',
            dataType: 'json',
            data: {technology: value,
                   project: projectId,
                   csrfmiddlewaretoken: CSRFToken},
            success: function (data, textStatus, xhr) {
                if (data.status == 401) {
                        location.href = data.redirect
                }
                else if (data.status === 500) {
                    $('#technology-error').removeClass('hidden');
                    $('#technology-error-message').text('Internal server error, please try again later.');
                }
                else if (data.content.success === true) {
                    $('#technology-error-message').addClass('hidden');

                    $('#technologies').append('<div id="technology-' + value + '" style="margin-bottom: 15px;">' +
                                                '<div>' +
                                                    '<p class="addedTechnology" id="technology-' + value + '-name">' +
                                                        '' + value + '' +
                                                        '<i id="technology-' + value + '-icon" class="fa fa-minus-circle" style="color: black; padding-left: 5px;" onclick="removeTechnology(&apos;' + value + '&apos;)"></i>' +
                                                    '<p>' +
                                                    '<p id="technology-' + value + '-error" class="hidden" style="text-align: center; color: red;">' +
                                                        '<i class="fa fa-exclamation-circle" style="color: red;"></i>' +
                                                        '<span id="technology-' + value + '-error-message"></span>' +
                                                    '</p>' +
                                                '</div>' +
                                                '<div>' +
                                                    '<div id="' + value + '-slider" class="technology-slider" data-name="' + value + '" data-strength="0"></div>' +
                                                '</div>' +
                                            '</div>');
                    $('#' + value + '-slider').slider({
                        min: 0,
                        max: 100,
                        value: 0,
                        change: function (event, ui) {
                            updateTechnology(value, $(this).slider( "value" ));
                        }
                    });
                    $('#technologyInput').val('');
                }
                else {
                    $('#technology-error').removeClass('hidden');
                    $('#technology-error-message').text(data.content.message);
                }

                showSaveToast('Technology');
            },
            error: function (xhr, textStatus, errorThrown) {
                $('#technology-error').removeClass('hidden');
                $('#technology-error-message').text('An error has occurred, we are working to fix it.');
            }
        });
    };

    var removeTechnology = function (value) {
         $.ajax({
            url: removeTechnologyURL,
            type: 'POST',
            dataType: 'json',
            data: {technology: value,
                   project: projectId,
                   csrfmiddlewaretoken: CSRFToken},
            success: function (data, textStatus, xhr) {
                if (data.status == 401) {
                    window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                }
                else if (data.status === 500) {
                    $('#technology-' + value + '-error').removeClass('hidden');
                    $('#technology-' + value + '-error-message').text('Internal server error, please try again later.');
                }
                else if (data.content.success === true) {
                    $('#technology-' + value).remove();
                    showSaveToast('Technology');
                }
                else {
                    $('#technology-' + value + '-error').removeClass('hidden');
                    $('#technology-' + value + '-error-message').text(data.content.message);
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                $('#technology-' + value + '-error').removeClass('hidden');
                $('#technology-' + value + '-error-message').text('An error has occurred, we are working to fix it.');
            }
        });
    };

    var updateTechnology = function (name, strength) {
         $.ajax({
            url: updateTechnologyURL,
            type: 'POST',
            dataType: 'json',
            data: {technology: name,
                   strength: strength,
                   project: projectId,
                   csrfmiddlewaretoken: CSRFToken},
            success: function (data, textStatus, xhr) {
                if (data.status == 401) {
                    window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                }
                else if (data.status === 500) {
                    $('#technology-' + name + '-error').removeClass('hidden');
                    $('#technology-' + name + '-error-message').text('Internal server error, please try again later.');
                }
                else if (data.content.success !== true) {
                    $('#technology-' + name + '-error').removeClass('hidden');
                    $('#technology-' + name + '-error-message').text(data.content.message);
                }
                showSaveToast('Technology');
            },
            error: function (xhr, textStatus, errorThrown) {
                $('#technology-' + name + '-error').removeClass('hidden');
                $('#technology-' + name + '-error-message').text('An error has occurred, we are working to fix it.');
            }
        });
    };

    $('#tags-input').on('beforeItemAdd', function(event) {
            $.ajax({
                url: addTagURL,
                type: 'POST',
                dataType: 'json',
                data: {tag: event.item,
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                    if (data.status == 401) {
                        window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                    }
                    else if (data.status === 500) {
                        $('#tags-error').removeClass('hidden');
                        $('#tags-error-message').text('Internal server error, please try again later.');
                    }
                    else if (data.content.success === true) {
                        $('#tags-error').addClass('hidden')
                    }
                    else {
                        $('tags-input').tagsinput('remove', event.item);
                        $('#tags-error').removeClass('hidden');
                        $('#tags-error-message').text(data.content.message);
                    }

                    showSaveToast('Tag');
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('tags-input').tagsinput('remove', event.item);
                    $('#tags-error').removeClass('hidden');
                    $('#tags-error-message').text('An error has occurred, we are working to fix it.');
                }
            });
    });

    $('#tags-input').on('beforeItemRemove', function(event) {
        $.ajax({
            url: removeTagURL,
            type: 'POST',
            dataType: 'json',
            data: {tag: event.item,
                   project: projectId,
                   csrfmiddlewaretoken: CSRFToken},
            success: function (data, textStatus, xhr) {
                if (data.status == 401) {
                    window.location.href = window.location.pathname.substring( 0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                }
                else if (data.status === 500) {
                    $('#tags-error').removeClass('hidden');
                    $('#tags-error-message').text('Internal server error, please try again later.');
                }
                else if (data.content.success === true) {
                    $('#tags-error').addClass('hidden')
                }
                else {
                    $('tags-input').tagsinput('add', event.item);
                    $('#tags-error').removeClass('hidden');
                    $('#tags-error-message').text(data.content.message);
                }

                showSaveToast('Tag');
            },
            error: function (xhr, textStatus, errorThrown) {
                $('tags-input').tagsinput('add', event.item);
                $('#tags-error-message').removeClass('hidden');
                $('#tags-error-message').text('An error has occurred, we are working to fix it.');
            }
        });
    });

    var updateProject = function (data) {
        $.ajax({
                url: updateProjectURL,
                type: 'POST',
                dataType: 'json',
                data: {data: JSON.stringify(data),
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                   if (data.status == 401) {
                        window.location.href = window.location.pathname.substring(0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                   }
                   else if (data.status === 500) {
                        $('#social-link-error-main').removeClass('hidden');
                        $('#social-link-error-main-message').text('Internal server error, please try again later.');
                   }
                   else if (data.content.success === true) {
                       $('#social-link-error-main').addClass('hidden');
                   }
                   else {
                        $('#social-link-error-main').removeClass('hidden');
                        $('#social-link-error-main-message').text(data.content.message);
                   }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#social-link-error-main').removeClass('hidden');
                    $('#social-link-error-main-message').text('An error has occurred, we are working to fix it.');
                }
            });
    };

    var editRepoURL = function (name, link) {
        var input = $('#' + name + '-input');

        if (input.val() == '') {
            if (link === '("")') {
                input.val('https://github.com/')
            }
            else {
                input.val(link);
            }
        }

        $('#div-' + name + '-repo').removeClass('hidden');
    };

    var updateRepo = function (link, name) {
        var input = $('#id_' + name),
            icon = $('#link-' + name),
            inputDiv = $('#div-' + name + '-repo'),
            errorMessageDiv = $('#' + name + '-repo-error'),
            valid = false;

        if ((link.startsWith('http://www.' + name + '.com/')
                    || link.startsWith('https://www.' + name + '.com/')
                    || link.startsWith('www.' + name + '.com/'))
                    || (link.startsWith('http://' + name + '.com/')
                    || link.startsWith('https://' + name + '.com/')
                    || link.startsWith(name + '.com/'))
                  && (!link.endsWith('.com/') && !link.endsWith('.com'))){
            valid = true;
        }

        if (valid) {
            inputDiv.addClass('hidden');

            saveRepoUpdate({'field': name, 'value': link});

            inputDiv.removeClass('has-error');
            errorMessageDiv.addClass('hidden');
        }
        else {
            inputDiv.addClass('has-error');

            var errorMessage = $('#' + name + '-repo-error-message');
            errorMessage.text('Please enter a valid ' + name + ' link');

            errorMessageDiv.removeClass('hidden');
        }
    };

    var saveRepoUpdate = function (data) {
        $.ajax({
                url: updateRepoURL,
                type: 'POST',
                dataType: 'json',
                data: {data: JSON.stringify(data),
                       project: projectId,
                       csrfmiddlewaretoken: CSRFToken},
                success: function (data, textStatus, xhr) {
                   if (data.status == 401) {
                        window.location.href = window.location.pathname.substring(0, window.location.pathname.indexOf( '/' ) + 1 ) + data.redirect
                   }
                   else if (data.status === 500) {
                        $('#repo-link-error-main').removeClass('hidden');
                        $('#repo-link-error-main-message').text('Internal server error, please try again later.');
                   }
                   else if (data.content.success === true) {
                       $('#repo-link-error-main').addClass('hidden');
                       showSaveToast('Repository');
                   }
                   else {
                        $('#repo-link-error-main').removeClass('hidden');
                        $('#repo-link-error-main-message').text(data.content.message);
                   }
                },
                error: function (xhr, textStatus, errorThrown) {
                    $('#repo-link-error-main').removeClass('hidden');
                    $('#repo-link-error-main-message').text('An error has occurred, we are working to fix it.');
                }
            });
    };

    var editSocialURL = function (name, link) {
        var input = $('#id_' + name);
        if (input.val() == '') {
            input.val(link);
        }

        $('#div-' + name ).removeClass('hidden');
    };

    var updateSocialKeyUp = function (name) {
        if (event.keyCode == 13) {
            updateSocialURL(name);
        }
    };

    var updateSocialURL = function (name) {
        var input = $('#id_' + name),
                link = input.val(),
                icon = $('#link-' + name),
                inputDiv = $('#div-' + name),
                errorMessageDiv = $('#social-link-error'),
                errorMesage = $('#social-link-error-' + name),
                valid = false;

        if (name === 'google-plus'
                && (link.startsWith('http://plus.google.com/')
                    || link.startsWith('https://plus.google.com/')
                    || link.startsWith('www.plus.google.com/'))
                && (!link.endsWith('.com/') && !link.endsWith('.com'))){
            valid = true;
        }
        else if ((link.startsWith('http://www.' + name + '.com/')
                    || link.startsWith('https://www.' + name + '.com/')
                    || link.startsWith('www.' + name + '.com/'))
                  && (!link.endsWith('.com/') && !link.endsWith('.com'))){
            valid = true;
        }

        if (valid) {
            $('#div-' + name).addClass('hidden');

            icon.removeClass('grey');
            icon.addClass(name);

            updateProject({'field': name, 'value': link})

            inputDiv.removeClass('has-error');
            errorMesage.addClass('hidden');
        }
        else {
            inputDiv.addClass('has-error');

            errorMessageDiv.removeClass('hidden');
            errorMesage.removeClass('hidden');
        }
    };

    $("#id_facebook").keyup(function () {
        updateSocialKeyUp('facebook');
    });
    $("#id_google-plus").keyup(function () {
        updateSocialKeyUp('google-plus');
    });
    $("#id_instagram").keyup(function () {
        updateSocialKeyUp('instagram');
    });
    $("#id_pinterest").keyup(function () {
        updateSocialKeyUp('pinterest');
    });
    $("#id_twitter").keyup(function () {
        updateSocialKeyUp('twitter');
    });

    $('.creator-edit').each(function(){
        $(this).editable({
            imageUpload: false,
            imageLink: false,
            buttons: ['bold', 'italic', 'underline', 'fontSize', 'sep', 'formatBlock',
                      'blockStyle', 'align',  'outdent', 'indent', 'sep', 'undo', 'redo'],
            saveParams: {
                csrfmiddlewaretoken: CSRFToken,
                field: 'summary',
                project: projectId,
                username: this.parentElement.id
            },
            saveURL: updateCreatorURL,
            autosave: true,
            autosaveInterval: 2500,
            crossDomain: false,
            placeholder: "Add a description of this creator's contribution"
        });
    });

    $('.technology-slider').each(function() {
        $(this).slider({
            min: 0,
            max: 100,
            value: $(this).data("strength"),
            change: function (event, ui) {
                updateTechnology($(this).data("name"), $(this).slider( "value" ));
            }
        });
    });

    $('.pitch-edit').each(function() {
        simpleEdit($(this), {'field': 'pitch'}, updateProjectURL, 'Create a pitch for your project it can include images, videos and embeded youtube content')
    });
    $('.project-tagline').each(function() {
        LimitedCharEdit($(this),  {'field': 'tagline'}, updateProjectURL, 'Provide a tag line for your project', 128)
    });
    $('.project-title').each(function() {
        LimitedCharEdit($(this),  {'field': 'title'}, updateProjectURL, 'Name your project', 64)
    });

    $('.post-title-edit').each(function() {
        simpleEdit($(this),  {'field': 'title', 'post': this.id}, updatePostURL, titlePlaceholder)
    });
    $('.post-edit').each(function() {
        richEdit($(this), {'field': 'post', 'post': this.id}, updatePostURL, postPlaceholder)
    });

    $('.post-title-edit').find('.fr-placeholder').each(function() {
        $(this).css('color', 'black');
    });

    $('.creator-edit').find('.fr-placeholder').each(function() {
        $(this).css('color', 'white');
    });

    toastr.options.closeButton = true;
    toastr.options.timeOut = 10000;
    toastr.options.fadeOut = 250;
    toastr.options.fadeIn = 250;
    toastr.options.positionClass = 'toast-bottom-right';
    toastr['info']("To edit your project simply click on the element you would like to change and start making your update.", "Updating your project");
