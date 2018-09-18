/**
 * Created by root on 17.9.18.
 */


function UploadFiles(dropZoneId, buttonId, mouseOverClass, skipFiles, fileContaner) {
    var dropZone = $("#" + dropZoneId);
    var ooleft = dropZone.offset().left;
    var ooright = dropZone.outerWidth() + ooleft;
    var ootop = dropZone.offset().top;
    var oobottom = dropZone.outerHeight() + ootop;
    var inputFile = dropZone.find("input");

    var filesArr = [];
    var fileLoads = [];
    var finalFiles = [];

    function showFiles() {
        $('#' + fileContaner).html("");
        var fileNum = filesArr.length;
        for (var i = 0; i < fileNum; i++) {

            objectURL = URL.createObjectURL(filesArr[i]);

            $('#' + fileContaner).append('<div><img title="' + filesArr[i].name + '" id="' + objectURL + '" src="' + objectURL + '" class="pre-visualizacao"><span class="fa-stack fa-lg"><i class="fa fa-file fa-stack-1x "></i><strong class="fa-stack-1x" style="color:#FFF; font-size:12px; margin-top:2px;">' + i + '</strong></span> ' + filesArr[i].name + '&nbsp;&nbsp;<span class="closeBtn" title="Remover">X</span></div>');

        }
    }

    function addFiles(e) {
        var tmp;

        // transfer dropped content to temporary array
        if (e.dataTransfer) {
            tmp = e.dataTransfer.files;
        } else if (e.target) {
            tmp = e.target.files;
        }

        // Copy the file items into the array
        for (var i = 0; i < tmp.length; i++) {
            filesArr.push(tmp.item(i));
            //console.log(i);
        }

        // remove all contents from the input elemnent (reset it)
        inputFile.wrap('<form>').closest('form').get(0).reset();
        inputFile.unwrap();

        showFiles();
    }


    $(function () {
        document.getElementById(dropZoneId).addEventListener("dragover", function (e) {
            e.preventDefault();
            e.stopPropagation();
            dropZone.addClass(mouseOverClass);
            var x = e.pageX;
            var y = e.pageY;

            if (!(x < ooleft || x > ooright || y < ootop || y > oobottom)) {
                inputFile.offset({
                    top: y - 15,
                    left: x - 100
                });
            } else {
                inputFile.offset({
                    top: -400,
                    left: -400
                });
            }

        }, true);

        if (buttonId != "") {
            var clickZone = $("#" + buttonId);

            var oleft = clickZone.offset().left;
            var oright = clickZone.outerWidth() + oleft;
            var otop = clickZone.offset().top;
            var obottom = clickZone.outerHeight() + otop;

            $("#" + buttonId).mousemove(function (e) {
                var x = e.pageX;
                var y = e.pageY;
                if (!(x < oleft || x > oright || y < otop || y > obottom)) {
                    inputFile.offset({
                        top: y - 15,
                        left: x - 160
                    });
                } else {
                    inputFile.offset({
                        top: -400,
                        left: -400
                    });
                }
            });
        }

        document.getElementById(dropZoneId).addEventListener("drop", function (e) {
            $("#" + dropZoneId).removeClass(mouseOverClass);
            addFiles(e);
        }, true);

        $('#' + fileContaner).on('click', '.closeBtn', function (e) {
            e.preventDefault();
            e.stopPropagation();
            var divElem = $(this).parent();
            var index = $('#' + fileContaner).find('div').index(divElem);
            if (index !== -1) {
                $('#' + fileContaner)[0].removeChild(divElem[0]);
                filesArr.slice(index, 1);
                fileLoads.splice(fileLoads.indexOf(this.id), 1);
            }

            document.getElementById(skipFiles).value = JSON.stringify(fileLoads);
        });

        inputFile.on('change', function (e) {
            $('#' + fileContaner).html("");
            var fileNum = this.files.length,
                initial = 0,
                counter = 0;
            for (initial; initial < fileNum; initial++) {
                counter = counter + 1;
                objectURL = URL.createObjectURL(this.files[initial]);
                $('#' + fileContaner).append('<div><img title="' + this.files[initial].name + '" id="' + objectURL + '" src="' + objectURL + '" class="pre-visualizacao"><span class="fa-stack fa-lg"><i class="fa fa-file fa-stack-1x "></i><strong class="fa-stack-1x" style="color:#FFF; font-size:12px; margin-top:2px;">' + counter + '</strong></span> ' + this.files[initial].name + '&nbsp;&nbsp;<span class="closeBtn" title="Remover">X</span></div>');
            }
        });

        inputFile.on('change', function (e) {
            finalFiles = {};
            fileLoads = [];
            $('#' + fileContaner).html("");
            var fileNum = this.files.length,
                initial = 0,
                counter = 0;

            $.each(this.files, function (idx, elm) {
                fileLoads[idx] = elm.name;
                finalFiles[idx] = elm;
            });


            for (initial; initial < fileNum; initial++) {
                counter = counter + 1;
                $('#' + fileContaner).append('<div><span class="fa-stack fa-lg"><i class="fa fa-file fa-stack-1x "></i><strong class="fa-stack-1x" style="color:#FFF; font-size:12px; margin-top:2px;">' + counter + '</strong></span> ' + this.files[initial].name + '&nbsp;&nbsp;<span class="closeBtn" title="Remover" id="'+ this.files[initial].name +'">X</span></div>');
            }

            document.getElementById(skipFiles).value = JSON.stringify(fileLoads);
        });


    })
}