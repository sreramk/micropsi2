var scene, camera, renderer;

var eye_background_color = new THREE.Color(0xFFFFFF);
var pup_color = new THREE.Color(0x523D89);
var nose_color = new THREE.Color(0x694032);
var mouth_color = new THREE.Color(0x764237);

var eye_l_width = 200;
var eye_l_height = 100;
var eye_l_x = -400 + (eye_l_width / 2) + 100;
var eye_l_y = -400 + (eye_l_height / 2) + 300;
var eye_r_width = 200;
var eye_r_height = 100;
var eye_r_x = -400 + (eye_r_width / 2) + 500;
var eye_r_y = -400 + (eye_r_height / 2) + 300;

var pup_l_width = 100;
var pup_l_height = 100;
var pup_l_x = -400 + (pup_l_width / 2) + 200;
var pup_l_y = -400 + (pup_l_height / 2) + 300;
var pup_r_width = 100;
var pup_r_height = 100;
var pup_r_x = -400 + (pup_r_width / 2) + 500;
var pup_r_y = -400 + (pup_r_height / 2) + 300;

var nose_width = 200;
var nose_height = 100;
var nose_x = -400 + (nose_width / 2) + 300;
var nose_y = -400 + (nose_height / 2) + 200;

var mouth_width = 400;
var mouth_height = 100;
var mouth_x = -400 + (mouth_width / 2) + 200;
var mouth_y = -400 + (mouth_height / 2) + 100;

var currentNodenet = $.cookie('selected_nodenet') || '';
var emoexpression = {}

var faceVertexShader = [
"varying vec2 vUv;",
"void main() {",
"vUv = uv;",
"gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );",
"}"
].join("\n");

var faceFragmentShader = [
"uniform sampler2D map;",
"uniform vec3 color;",
"varying vec2 vUv;",
"void main() {",
"vec4 texel = texture2D( map, vUv );",
"gl_FragColor = vec4( texel.xyz + color, texel.w );",
"}"
].join("\n")

init();
register_stepping_function('nodenet', get_nodenet_data, fetchEmoexpressionParameters)

animate();

function init() {

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 1, 10000 );
    camera.position.z = 2000;

    texture = THREE.ImageUtils.loadTexture('/static/face/stevehead.png'),
    textureMaterial = new THREE.ShaderMaterial();

    face_background_p = new THREE.PlaneGeometry( 800, 800 )
    face_background_m = new THREE.ShaderMaterial({
        uniforms: {
            map: {type: 't', value: texture},
            color: {type: 'c', value: new THREE.Color( 0x000000 )}
        },
     	vertexShader: faceVertexShader,
        fragmentShader: faceFragmentShader,
        transparent: false
    });

    face_background = new THREE.Mesh( face_background_p, face_background_m );
    scene.add( face_background );

    eye_l_p = new THREE.PlaneGeometry( eye_l_width, eye_l_height )
    eye_l_m = new THREE.MeshBasicMaterial( { color: eye_background_color, wireframe: false } );
    eye_l = new THREE.Mesh( eye_l_p, eye_l_m );
    eye_l.position.x = eye_l_x;
    eye_l.position.y = eye_l_y;
    scene.add( eye_l );

    eye_r_p = new THREE.PlaneGeometry( eye_r_width, eye_r_height )
    eye_r_m = new THREE.MeshBasicMaterial( { color: eye_background_color, wireframe: false } );
    eye_r = new THREE.Mesh( eye_r_p, eye_r_m );
    eye_r.position.x = eye_r_x;
    eye_r.position.y = eye_r_y;
    scene.add( eye_r );

    pup_l_p = new THREE.PlaneGeometry( pup_l_width, pup_l_height )
    pup_l_m = new THREE.MeshBasicMaterial( { color: pup_color, wireframe: false } );
    pup_l = new THREE.Mesh( pup_l_p, pup_l_m );
    pup_l.position.x = pup_l_x;
    pup_l.position.y = pup_l_y;
    scene.add( pup_l );

    pup_r_p = new THREE.PlaneGeometry( pup_r_width, pup_r_height )
    pup_r_m = new THREE.MeshBasicMaterial( { color: pup_color, wireframe: false } );
    pup_r = new THREE.Mesh( pup_r_p, pup_r_m );
    pup_r.position.x = pup_r_x;
    pup_r.position.y = pup_r_y;
    scene.add( pup_r );

    nose_p = new THREE.PlaneGeometry( nose_width, nose_height )
    nose_m = new THREE.MeshBasicMaterial( { color: nose_color, wireframe: false } );
    nose = new THREE.Mesh( nose_p, nose_m );
    nose.position.x = nose_x;
    nose.position.y = nose_y;
    scene.add( nose );

    mouth_p = new THREE.PlaneGeometry( mouth_width, mouth_height )
    mouth_m = new THREE.MeshBasicMaterial( { color: mouth_color, wireframe: false } );
    mouth = new THREE.Mesh( mouth_p, mouth_m );
    mouth.position.x = mouth_x;
    mouth.position.y = mouth_y;
    scene.add( mouth );

    canvas = document.getElementById("face");

    renderer = new THREE.WebGLRenderer({canvas: canvas});
    renderer.setSize( canvas.width * 4, canvas.height * 4)

}

function animate() {

    requestAnimationFrame( animate );

    //face_background_m.uniforms["color"]["value"] = new THREE.Color( Math.random(), -0.8, -0.8 )

    renderer.render( scene, camera );

}

function get_nodenet_data(){
    return {
        'nodespace': "Root",
        'step': 0,              // todo: do we need to know the current netstep -1?
        'coordinates': {
            x1: 0,
            x2: 0,
            y1: 0,
            y2: 0
        }
    }
}

function fetchEmoexpressionParameters() {
    api.call('get_emoexpression_parameters', {nodenet_uid:currentNodenet}, success=function(data){
        emoexpression = data;
        updateEmoexpressionParameters(data)
    });
}

function updateEmoexpressionParameters(data) {

    var table = $('table.emoexpression');
    html = '';
    var sorted = [];
    globalDataSources = [];
    globalDataTargets = [];

    for(key in data){
        sorted.push({'name': key, 'value': data[key]});
    }
    sorted.sort(sortByName);
    // display reversed to get emo_ before base_
    for(var i = sorted.length-1; i >=0; i--){
        html += '<tr><td>'+sorted[i].name+'</td><td>'+sorted[i].value.toFixed(2)+'</td><td><!--button class="btn btn-mini" data="'+sorted[i].name+'">monitor</button--></td></tr>'
        if(sorted[i].name.substr(0, 3) == "emo"){
            globalDataSources.push(sorted[i].name);
        } else {
            globalDataTargets.push(sorted[i].name);
        }
    }
    table.html(html);
    /*
    $('button', table).each(function(idx, button){
        $(button).on('click', function(evt){
            evt.preventDefault();
            var mod = $(button).attr('data');
            api.call('add_modulator_monitor', {
                    nodenet_uid: currentNodenet,
                    modulator: mod,
                    name: mod
                }, function(data){
                    dialogs.notification('Monitor added', 'success');
                    $(document).trigger('monitorsChanged', data);
                }
            );
        });
    });
    */
}