editor = null
currentPatch = ''

function sendCmd(cmd) {
    $.post("http://raspberrypi.local:8080/send_command", { data: cmd })
    .done(function(data) {
         // alert(data);
    });
}

function getPatch(patch) {
    $.get('http://raspberrypi.local:8080/get_patch/' + patch, function(data) {
        editor.setValue(data)
        editor.gotoLine(1)
        currentPatch = patch
        $("#title").html(patch)
    });
}

function getPatchList() {
     $.getJSON('http://raspberrypi.local:8080', function(data) {
        $("#patches").empty();
        $.each(data, function (i,v) {
          
            $patch = $('<div class="side-button"></div>').append(v);
            $patch.click(function () {
                getPatch(v);
            });
           $("#patches").append($patch);
        });
    });
}

function saveNewPatch() {
    
    newName = prompt('Enter New Name (No Spaces!)')

    $.post("http://raspberrypi.local:8080/save_new", { name: newName, contents: editor.getValue() })
    .done(function(data) {
        // reload patch list
        getPatchList();
         // alert(data);
    });
}

function savePatch() {
    
    $.post("http://raspberrypi.local:8080/save", { name: currentPatch, contents: editor.getValue() })
    .done(function(data) {
         // alert(data);
    });
}

$(document).ready(function() {
    
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/merbivore_soft");
    editor.getSession().setMode("ace/mode/python");
    //$("#editor").style.fontSize='16px';
    document.getElementById('editor').style.fontSize='14px';
    getPatchList();

    $("#clear-screen").click(function() {
        sendCmd("cs\n");
    });


    $("#reload-patch").click(function() {
        sendCmd("rlp\n");
    });


    $("#osd-toggle").click(function() {
        sendCmd("osd\n");
    });

    $("#quit").click(function() {
        sendCmd("quit\n");
    });



    $("#save-new").click(function() {
        saveNewPatch();
    });



    $("#save").click(function() {
        savePatch();
    });

});
