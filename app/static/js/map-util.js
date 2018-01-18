/**
 * Created by Administrator on 2014-11-13.
 */
var map_style = '<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />';
map_style += '<style type="text/css">body, html,#allmap {width: 100%;height: 100%;overflow: hidden;margin:0;font-family:"微软雅黑";}</style>';
map_style += '<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=dqeWbjwfiNYG4uVihtEBlXpX"></script>';
map_style += '<script type="text/javascript" src="http://api.map.baidu.com/library/DistanceTool/1.2/src/DistanceTool_min.js"></script>';
document.write(map_style);
createMap = function (divName) {
    var me = this;
    var map = new BMap.Map(divName);    // 创建Map实例
    if (map == null) {
        return;
    }
    map.addControl(new BMap.MapTypeControl());   //添加地图类型控件
    var menu = new BMap.ContextMenu();
    var myDis = new BMapLib.DistanceTool(map);
    var txtMenuItem = [
        {
            text: '搜索',
            callback: function () {
                Ext.Msg.prompt('搜索', '输入名称:', function (btn, text) {
                    if (btn == 'ok') {
                        if (text != "") {
                            map.centerAndZoom(text, 11);
                        }
                    }
                });
            }
        },
        {
            text: '测量',
            callback: function () {
                myDis.open();
            }
        }
    ];
    for (var i = 0; i < txtMenuItem.length; i++) {
        menu.addItem(new BMap.MenuItem(txtMenuItem[i].text, txtMenuItem[i].callback, 100));
    }
    map.addContextMenu(menu);
    var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
    var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件
    var top_right_navigation = new BMap.NavigationControl({anchor: BMAP_ANCHOR_TOP_RIGHT, type: BMAP_NAVIGATION_CONTROL_SMALL}); //右上角，仅包含平移和缩放按钮
    map.addControl(top_left_control);
    map.addControl(top_left_navigation);
    map.addControl(top_right_navigation);
    map.enableScrollWheelZoom();   //启用滚轮放大缩小，默认禁用
    map.enableContinuousZoom();    //启用地图惯性拖拽，默认禁用
    return map;
}
function drawingManager(map, overlays) {
    var overlaycomplete = function (e) {
        e.overlay.enableEditing();
        overlays.push(e.overlay);
        var markerMenu = new BMap.ContextMenu();
        markerMenu.addItem(new BMap.MenuItem('删除', removeMarker.bind(e.overlay)));
        e.overlay.addContextMenu(markerMenu);
    };
    var styleOptions = {
        strokeColor: "red",    //边线颜色。
        fillColor: "red",      //填充颜色。当参数为空时，圆形将没有填充效果。
        strokeWeight: 3,       //边线的宽度，以像素为单位。
        strokeOpacity: 0.8,	   //边线透明度，取值范围0 - 1。
        fillOpacity: 0.6,      //填充的透明度，取值范围0 - 1。
        strokeStyle: 'solid' //边线的样式，solid或dashed。
    }
    //实例化鼠标绘制工具
    var drawingManager = new BMapLib.DrawingManager(map, {
        isOpen: false, //是否开启绘制模式
        enableDrawingTool: true, //是否显示工具栏
        drawingToolOptions: {
            anchor: BMAP_ANCHOR_TOP_RIGHT, //位置
            offset: new BMap.Size(200, 5),//偏离值
            drawingModes: [
                BMAP_DRAWING_CIRCLE,
                BMAP_DRAWING_POLYGON
            ]
        },
        enableCalculate: false,
        circleOptions: styleOptions, //圆的样式
        polylineOptions: styleOptions, //线的样式
        polygonOptions: styleOptions, //多边形的样式
        rectangleOptions: styleOptions //矩形的样式
    });
    //添加鼠标绘制工具监听事件，用于获取绘制结果
    drawingManager.addEventListener('overlaycomplete', overlaycomplete);
    function clearAll() {
        for (var i = 0; i < overlays.length; i++) {
            map.removeOverlay(overlays[i]);
        }
        overlays.length = 0
    }

    var removeMarker = function (e, ee, marker) {
        map.removeOverlay(marker);
        Ext.Array.remove(overlays, marker);
    }
}
function initCanEditMap(cur_map, record, overlays) {
    cur_map.setCurrentCity("北京");
    drawingManager(cur_map, overlays)
    if (record) {
        var county = record.get("county");
        //cur_map.centerAndZoom(county, 11);
        var marks = record.get("marks");
        var removeMarker = function (e, ee, marker) {
            cur_map.removeOverlay(marker);
            Ext.Array.remove(overlays, marker);
        }
        var longitude = record.get("longitude");
        var latitude = record.get("latitude");
        var radius = record.get("radius");
        if (longitude - 0.001 > 0) {
            var point = new BMap.Point(longitude, latitude);
            var circle = new BMap.Circle(point, radius, {fillColor: "red", fillOpacity: 0.2, strokeColor: "red", strokeWeight: 2, strokeOpacity: 0.5}); //创建圆
            cur_map.addOverlay(circle);
            overlays.push(circle);
            circle.enableEditing();
            var markerMenu = new BMap.ContextMenu();
            markerMenu.addItem(new BMap.MenuItem('删除', removeMarker.bind(circle)));
            circle.addContextMenu(markerMenu);
            cur_map.centerAndZoom(point, 11);
        }
        Ext.each(marks, function (mark) {
            if (mark[0] == 1) {
                var m = mark[1][0];
                //var xyr=point_str.split(',');
                var point = new BMap.Point(m[0], m[1]);
                var circle = new BMap.Circle(point, m[2], {fillColor: "red", fillOpacity: 0.2, strokeColor: "red", strokeWeight: 2, strokeOpacity: 0.5}); //创建圆
                cur_map.addOverlay(circle);
                overlays.push(circle);
                circle.enableEditing();
                var markerMenu = new BMap.ContextMenu();
                markerMenu.addItem(new BMap.MenuItem('删除', removeMarker.bind(circle)));
                circle.addContextMenu(markerMenu);
                cur_map.centerAndZoom(point, 11);
            } else if (mark[0] == 2) {
                var xys = mark[1];
                var points = [];
                Ext.each(xys, function (xy) {
                    var point = new BMap.Point(xy[0], xy[1]);
                    points.push(point);
                })
                if(points.length>0) {
                    var polygon = new BMap.Polygon(points, {fillColor: "red", fillOpacity: 0.2, strokeColor: "red", strokeWeight: 2, strokeOpacity: 0.5});
                    cur_map.addOverlay(polygon);
                    overlays.push(polygon);
                    polygon.enableEditing();
                    var markerMenu = new BMap.ContextMenu();
                    markerMenu.addItem(new BMap.MenuItem('删除', removeMarker.bind(polygon)));
                    polygon.addContextMenu(markerMenu);
                     cur_map.centerAndZoom(points[0], 11);
                }
            }
        })
    } else {
        var area_name = parent.userManager.currentUser.company_county;
        cur_map.centerAndZoom(area_name, 11);
    }
}
function initFixedMap(cur_map,record, overlays) {
    cur_map.setCurrentCity("北京");
    //drawingManager(cur_map, overlays)
    if (record) {
        var county = record.get("county");
        //cur_map.centerAndZoom(county, 11);
        var marks = record.get("marks");
        var longitude = record.get("longitude");
        var latitude = record.get("latitude");
        var radius = record.get("radius");
        if (longitude - 0.001 > 0) {
            var point = new BMap.Point(longitude, latitude);
            var circle = new BMap.Circle(point, radius, {fillColor: "red", fillOpacity: 0.2, strokeColor: "red", strokeWeight: 2, strokeOpacity: 0.5}); //创建圆
            cur_map.addOverlay(circle);
            overlays.push(circle);
            cur_map.centerAndZoom(point, 11);
        }
        Ext.each(marks, function (mark) {
            if (mark[0] == 1) {
                var m = mark[1][0];
                //var xyr=point_str.split(',');
                var point = new BMap.Point(m[0], m[1]);
                var circle = new BMap.Circle(point, m[2], {fillColor: "red", fillOpacity: 0.2, strokeColor: "red", strokeWeight: 2, strokeOpacity: 0.5}); //创建圆
                cur_map.addOverlay(circle);
                overlays.push(circle);
                cur_map.centerAndZoom(point, 11);
            } else if (mark[0] == 2) {
                var xys = mark[1];
                var points = [];
                Ext.each(xys, function (xy) {
                    var point = new BMap.Point(xy[0], xy[1]);
                    points.push(point);
                })
                if(points.length>0){
                    var polygon = new BMap.Polygon(points, {fillColor: "red", fillOpacity: 0.2, strokeColor: "red", strokeWeight: 2, strokeOpacity: 0.5});
                    cur_map.addOverlay(polygon);
                    overlays.push(polygon);
                    cur_map.centerAndZoom(points[0], 11);
                }
            }
        })
    } else {
        var area_name = parent.userManager.currentUser.company_county;
        cur_map.centerAndZoom(area_name, 11);
    }
}
BaiDuMapToGps = function (base_point, call_back) {
    var me = this;
    setTimeout(function () {
        var convertor = new BMap.Convertor();
        var pointArr = [];
        pointArr.push(base_point);
        convertor.translate(pointArr, 1, 5, function (data) {
            if (data.status === 0) {
                var point = data.points[0];
                var x = 2 * base_point.lng - point.lng
                var y = 2 * base_point.lat - point.lat
                if (call_back) {
                    call_back(x, y);
                }
            }
        }, 2000);
    });
}
GpsToBaiDu = function (base_point, call_back) {
    var me = this;
    setTimeout(function () {
        var convertor = new BMap.Convertor();
        var pointArr = [];
        pointArr.push(base_point);
        convertor.translate(pointArr, 1, 5, function (data) {
            if (data.status === 0) {
                if (call_back) {
                    var point = data.points[0];
                    call_back(point);
                }
            }
        }, 1000);
    });
}
GpsPointsToBaiDu = function (pointArr, call_back) {
    var me = this;
    setTimeout(function () {
        var convertor = new BMap.Convertor();
        convertor.translate(pointArr, 1, 5, function (data) {
            if (data.status === 0) {
                if (call_back) {
                    var points = data.points;
                    call_back(points);
                }
            }
        }, 1000);
    });
}
/*function xyzTojwd(x1,y1,jdd,type,dk){
    var dh=0;
    var ipl=3.1415926535898/180;
    //dk=6; //'6度带宽
    var a= 0,f=0;
    if(type==54){
        a=6378245.0; //#'坐标系参数:54北京为6378245.0; 80西安为6378140.0
        f=1.0/298.3 ;//# '  坐标系参数:54北京为1.0/298.3; 80西安为1/298.257
    }else{
        a=6378140.0; //#'坐标系参数:54北京为6378245.0; 80西安为6378140.0
        f=1.0/298.257 ;//# '  坐标系参数:54北京为1.0/298.3; 80西安为1/298.257
    }
    dh=parseInt(y1/1000000);
    var l0=(dh-1)*dk+dk/2;
    l0=l0*ipl;
    var y0=1000000*dh+500000;
    var x0=0;
    x1=x1-x0;
    y1=y1-y0;
    var e2=2*f-f*f;
    var e1=(1-Math.sqrt(1-e2))/(1+Math.sqrt(1-e2));
    var ee=e2/(1.0-e2);
    var m=x1;
    var u=m/(a*(1-e2/4-3*e2*e2/64-5*e2*e2/256));
    var fai=u+(3*e1/2-27*e1*e1*e1/32)*Math.sin(2*u)+(21*e1*e1/16-55*e1*e1*e1*e1/32)*Math.sin(4*u)+(151*e1*e1*e1/96)*Math.sin(6*u)+(1097*e1*e1*e1*e1/512)*Math.sin(8*u);
    var c=ee*Math.cos(fai)*Math.cos(fai);
    var t=Math.tan(fai)*Math.tan(fai);
    var nn=a/Math.sqrt(1-e2*Math.sin(fai)*Math.sin(fai));
    var r=a*(1-e1)/Math.sqrt((1-e2*Math.sin(fai)*Math.sin(fai))*(1-e2*Math.sin(fai)*Math.sin(fai))*(1-e2*Math.sin(fai)*Math.sin(fai)));
    var d=y1/nn;  //#'计算经纬度
    var l1=l0+(d-(1+2*t+c)*d*d*d/6+(5-2*c+28*t-3*c*c+8*ee+24*t*t)*d*d*d*d*d/120)/Math.cos(fai);
    var b1=fai-(nn*Math.tan(fai)/r)*(d*d/2-(5+3*t+10*c-4*c*c-9*ee)*d*d*d*d/24+(61+90*t+298*c+45*t*t-256*ee-3*c*c)*d*d*d*d*d*d/720);//#   '转换为度
    l1=l1/ipl+jdd;
    b1=b1/ipl;
    return [l1,b1]
}
function jwdToxyz(l1,b1,jdd,type,dk){
    var dh=0;
    var l0=0.0,b0=0.0,x0=0.0,x1=0.0,y0=0.0,y1=0.0, a=0.0, f=0.0, e=0.0,ee=0.0,e2=0.0,nn=0.0, t=0.0, c=0.0,aa=0.0, m=0.0,ipl=0.0;
    ipl=3.14156926535898/180;
    //dk=6; //'6度带宽
    if(type==54){
        a=6378245.0; //#'坐标系参数:54北京为6378245.0; 80西安为6378140.0
        f=1.0/298.3 ;//# '  坐标系参数:54北京为1.0/298.3; 80西安为1/298.257
    }else{
        a=6378140.0; //#'坐标系参数:54北京为6378245.0; 80西安为6378140.0
        f=1.0/298.257 ;//# '  坐标系参数:54北京为1.0/298.3; 80西安为1/298.257
    }
    b0=0;
    l1=l1-jdd;
    dh=parseInt((l1+dk)/dk);
    l0=(dh-1)*dk+dk/2;
    l0=l0*ipl;
    y0=1000000*dh+500000;
    x0=0;

    l1=l1*ipl;
    b1=b1*ipl;
    e2=2*f-f*f;
    ee=e2*(1.0-e2);
    nn=a/Math.sqrt(1-e2*Math.sin(b1)*Math.sin(b1));
    t=Math.tan(b1)*Math.tan(b1);
    c=ee*Math.cos(b1)*Math.cos(b1);
    aa=(l1-l0)*Math.cos(b1);
    m=a*((1-e2/4-3*e2*e2/64-5*e2*e2*e2/256)*b1-(3*e2/8+3*e2*e2/32+45*e2*e2*e2/1024)*Math.sin(2*b1)+(15*e2*e2/256+45*e2*e2*e2/1024)*Math.sin(4*b1)-(35*e2*e2*e2/3072)*Math.sin(6*b1));
    y1=nn*(aa+(1-t+c)*aa*aa*aa/6+(5-18*t+t*t+72*c-58*ee)*aa*aa*aa*aa*aa/120);
    x1=m+nn*Math.tan(b1)*(aa*aa/2+(5-t+9*c+4*c*c)*aa*aa*aa*aa/24+(61-58*t+t*t+600*c-330*ee)*aa*aa*aa*aa*aa*aa/720);
    x1=x0+x1;
    y1=y0+y1;
    return [x1,y1]
}*/
function xy_to_jwd(X,Y,L0,type){
    var e=3.1415926/180;
    var p0=57.29577951308232;
    if(type==80) {
        var a = 6378140,
            c = 6399596.6519880105,
            E1 = 6.739501819473E-03,
            E = 6.694384999588E-03,
            a0 = 111133.0046793,
            a2 = -16038.52818,
            a4 = 16.83263,
            a6 = -2.198E-02,
            a8 = 3E-05,
            q0 = 157048687.47416E-15,
            q2 = 2526252791.9786E-12,
            q4 = -14923644.4356E-12,
            q6 = 120769.9608E-12,
            q8 = -1075.7700E-12;
    }else{
        var a=6378245,
        E1=6.738525414683E-03,
        E=6.693421622966E-03,
        c=6399698.901782711,
        a0=111134.8610828,
        a2=-16036.48022,
        a4=16.82805,
        a6=-2.197E-02,
        a8=3E-05,
        q0=157046064.12328E-15,
        q2=2525886946.8158E-12,
        q4=-14919317.6572E-12,
        q6=120717.4265E-12,
        q8=-1075.1509E-12;
    }
    var B0=X*q0
    var Bf=B0+Math.sin(2*B0)*(q2+Math.sin(B0)*Math.sin(B0)*(q4+Math.sin(B0)*Math.sin(B0)*(q6+q8*Math.sin(B0)*Math.sin(B0))))
    Y=Y-500000
    var tf=Math.tan(Bf)
    var k=E1*Math.cos(Bf)*Math.cos(Bf);
    var vf=1+k;
    var Nf=c/Math.sqrt(vf)
    var q=Y/Nf
    var B=Bf/e+p0*tf*(-vf+((5+3*tf*tf*(1+(-2-3*k)*k)+3*k*(2-k))+(-(61+45*tf*tf*(2+tf*tf)+(107+(-162-45*tf*tf)*tf*tf)*k)+(1385+(3633+(4095+1575*tf*tf)*tf*tf)*tf*tf)*q*q/56)*q*q/30)*q*q/12)*q*q/2;
    var l0=p0*q/Math.cos(Bf)*(1+(-(1+2*tf*tf+k)+((5+4*tf*tf*(7+6*tf*tf)+2*k*(3+4*tf*tf))-(61+(662+(1320+720*tf*tf)*tf*tf)*tf*tf)*q*q/42)*q*q/20)*q*q/6)
    var L=L0+l0
    return  [L,B]
}
function jwd_to_XY(jd,wd,L0,type){
    var e=3.1415926/180;
    var p0=57.29577951308232;
    if(type==80) {
        var a = 6378140,
            c = 6399596.6519880105,
            E1 = 6.739501819473E-03,
            E = 6.694384999588E-03,
            a0 = 111133.0046793,
            a2 = -16038.52818,
            a4 = 16.83263,
            a6 = -2.198E-02,
            a8 = 3E-05,
            q0 = 157048687.47416E-15,
            q2 = 2526252791.9786E-12,
            q4 = -14923644.4356E-12,
            q6 = 120769.9608E-12,
            q8 = -1075.7700E-12;
    }else{
        var a=6378245,
        E1=6.738525414683E-03,
        E=6.693421622966E-03,
        c=6399698.901782711,
        a0=111134.8610828,
        a2=-16036.48022,
        a4=16.82805,
        a6=-2.197E-02,
        a8=3E-05,
        q0=157046064.12328E-15,
        q2=2525886946.8158E-12,
        q4=-14919317.6572E-12,
        q6=120717.4265E-12,
        q8=-1075.1509E-12;
    }
    var t=Math.tan( jd*e)
    var k=E1*Math.cos( jd*e)*Math.cos( jd*e)
    var v=1+k
    var N=c/Math.sqrt(v)
    var l0=wd-L0
    var p=Math.cos( jd*e)*l0/p0
    var X=a0*jd+a2*Math.sin(2* jd*e)+a4*Math.sin(4*jd*e)+a6*Math.sin(6*jd*e)+a8*Math.sin(8*jd*e)
    var  R_X=X+N*t*(1+((5-t*t+(9+4*k)*k)+((61+(t*t-58)*t*t+(9-11*t*t)*30*k)+(1385+(-3111+(543-t*t)*t*t)*t*t)*p*p/56)*p*p/30)*p*p/12)*p*p/2
    var R_Y=500000+N*(1+((1-t*t+k)+((5+t*t*(t*t-18-58*k)+14*k)+(61+(-479+(179-t*t)*t*t)*t*t)*p*p/42)*p*p/20)*p*p/6)*p
    return  [R_X,R_Y]
}
//var t1=jwdToxyz(123.577,41.25,123,80,6);
//var t2=xyzTojwd(t1[0],t1[1],123,80,6);
//var t3=0;
