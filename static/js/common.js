/*tdplatform项目
* 
* 适用：本项目所有页面
* Date:2020-1-10
*/


function add_column(){
    var index = layer.open({
        type:1,
        skin:"layui-layer-rim",
        area:["400px","200px"],
        title:"新增栏目",
        content:'<div class="text-center" style="margin-top:20px"><p>请输入新的栏目名称</p><p>{{column_form.column}}</p></div>',
        btn:['确定', '取消'],
        yes: function(index, layero) {
          column_name = $('#id_column').val();
        //   alert(column_name);
          $.ajax({
              url:'{% url "article:article_column" %}',
              type:'POST',
              data:{"column":column_name},
              success:function(e) {
                if(e=="1"){
                    parent.location.reload();
                    layer.msg("good");
                }else{
                    layer.msg("此栏目已存在，请更换其他名称");
                }
              },
          });
        },
        btn2: function(index, layero) {
            layer.close(index);
        }
    });
};

function edit_column(the, column_id) {
    var name = $(the).parents("tr").children("td").eq(1).text();
    var index = layer.open({
        type: 1,
        skin: "layui-layer-rim",
        area: ["400px", "200px"],
        title: "编辑栏目",
        content: '<div class="text-center" style="margin-top:20px"><p>请编辑栏目</p><p><input type="text" id="new_name" value="' + name + '"></p></div>',
        btn: ['确定', '取消'],
        yes: function (index, layero) {
            new_name = $("#new_name").val();
            $.ajax({
                url: "{% url 'article:rename_article_column' %}",
                type: "POST",
                data: { "column_id": column_id, "column_name": new_name },
                success: function (e) {
                    if (e = "1") {
                        parent.location.reload();
                        layer.msg("good");
                    } else {
                        layer.msg("新的名称没有保存，保存失败。")
                    }
                },
            });
        },
    });
};

function delete_column(the, column_id) {
    var name = $(the).parents("tr").children("td").eq(1).text();
    layer.open({
        type:1,
        skin:"layui-layer-rim",
        area:["400px","200px"],
        title:"删除栏目",
        content:'<div class="text-center" style="margin-top:20px"><p>是否确定删除{'+name+'}栏目</p></div>',
        btn:['确定','取消'],
        yes: function() {
            $.ajax({
                url:"{% url 'article:del_article_column' %}",
                type:'POST',
                data:{"column_id":column_id},
                success: function (e) {
                    if (e="1") {
                        parent.location.reload();
                        layer.msg("good");
                    } else {
                        layer.msg("删除成功");
                    }
                },
            })
        }
    });
}


// 控制显示或隐藏密码
function show_pwd() {
    var login_pwd = $("#login_pwd")
    if (login_pwd.attr('type') == "password") {
        login_pwd.attr("type", "text");
    } else {
        login_pwd.attr("type", "password");
    }
}

// 添加优秀实践页面：通过联动框，选择作者
function handle() {
    var group =  $("#group_name").val()
    $.ajax({
        type:"post",
        url:"group_user",
        data:{"group_id":group},
        datatype:'json',
        success: function(e) {
            if(e!=null){
                var author = $("#id_author");
                var dataObj = eval(e);
                var dataArr = dataObj.data;
                author.empty();
                // console.log(dataArr)
                if(dataArr==null){
                    keshi.append("<option value = '-1'>"+"成员为空"+"</option>");
                }
                if (dataArr!=null) {
                    for(var i=0;i<dataArr.length;i++){
                        var item =dataArr[i];
                        author.append("<option value = '"+item.id+"'>"+item.realname+"</option>")
                    };
                }
            }
        }
    });
}

function change_teacher() {
    var group = $("#groups-user").val()
    $.ajax({
        type: "post",
        url: "../../asset/group_user",
        data: { "group_id": group },
        datatype: 'json',
        success: function (e) {
            if (e != null) {
                var author = $("#id_teacher");
                var dataObj = eval(e);
                var dataArr = dataObj.data;
                author.empty();
                console.log(dataArr)
                // console.log(dataArr)
                if (dataArr.length == 0) {
                    author.append("<option value = '-1'>" + "成员为空" + "</option>");
                }
                if (dataArr != null) {
                    for (var i = 0; i < dataArr.length; i++) {
                        var item = dataArr[i];
                        author.append("<option value = '" + item.id + "'>" + item.realname + "</option>")
                    };
                }
            }
        }
    });
}