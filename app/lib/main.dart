import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:webview_flutter/webview_flutter.dart';

/* import 'package:flutter_svg/flutter_svg.dart';

class MyIconWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('IGood to Cook'),
      ),
      body: Center(
        child: SvgPicture.asset(
          'assets/icono.svg', // Ruta de tu archivo SVG
          width: 100,
          height: 100, 
        ),
      ),
    );
  }
} */
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  CameraDescription firstCamera;

  if (cameras.isNotEmpty) {
    firstCamera = cameras.first;
  } else {
    print('No se encontraron cámaras disponibles en el dispositivo.');
    return;
  }
  runApp(CameraApp(firstCamera));
}

class CameraApp extends StatefulWidget {
  final CameraDescription camera;

  const CameraApp(this.camera);

  @override
  _CameraAppState createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  late CameraController _controller;
  XFile? _imageFile;
  bool _showWebView = false;
  WebViewController? _webViewController;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.max,
    );
    _controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    });
    // Agregar inicialización de WebView
    if (Platform.isAndroid) WebView.platform = SurfaceAndroidWebView();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _takePicture() async {
    if (!_controller.value.isInitialized) {
      return;
    }
    try {
      final XFile file = await _controller.takePicture();
      setState(() {
        _imageFile = file;
      });
    } catch (e) {
      print('Error al tomar la foto: $e');
    }
  }

  void _pickPictureFromGallery() async {
    try {
      final XFile? file =
          await ImagePicker().pickImage(source: ImageSource.gallery);
      if (file != null) {
        setState(() {
          _imageFile = file;
        });
      }
    } catch (e) {
      print('Error al seleccionar la foto de la galería: $e');
    }
  }

  void _discardPicture() {
    setState(() {
      _imageFile = null;
      _showWebView = false;
    });
  }

  void _goBack() {
    if (_webViewController != null) {
      _webViewController!.canGoBack().then((canGoBack) {
        if (canGoBack) {
          _webViewController!.goBack();
        } else {
          setState(() {
            _imageFile = null;
            _showWebView = false;
          });
        }
      });
    }
  }

  Future<void> _sendPicture() async {
    if (_imageFile != null) {
      try {
        print('Send image buttom');
        var uri = Uri.parse('http://192.168.18.16:12345/upload');
        var request = http.MultipartRequest('POST', uri)
          ..files.add(
            await http.MultipartFile.fromPath('image', _imageFile!.path),
          );

        var streamedResponse = await request.send();
        var response = await http.Response.fromStream(streamedResponse);

        if (response.statusCode == 200) {
          print('¡Imagen enviada con éxito!');
          setState(() {
            _showWebView = true;
          });
        } else {
          print('Error al enviar la imagen: ${response.reasonPhrase}');
        }
      } catch (e) {
        print('Error al enviar la imagen: $e');
      }
    } else {
      print('No hay ninguna imagen para enviar.');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_controller.value.isInitialized) {
      return Center(child: CircularProgressIndicator());
    }
    return MaterialApp(
      home: Scaffold(
        body: _showWebView
            ? WebView(
                initialUrl: 'http://192.168.18.16:8501',
                javascriptMode: JavascriptMode.unrestricted,
                onWebViewCreated: (controller) {
                  _webViewController = controller;
                })
            : Stack(
                fit: StackFit.expand,
                children: [
                  AspectRatio(
                    aspectRatio: _controller.value.aspectRatio,
                    child: CameraPreview(_controller),
                  ),
                  if (_imageFile != null)
                    Positioned.fill(
                      child: Image.file(
                        File(_imageFile!.path),
                        fit: BoxFit.cover,
                      ),
                    ),
                  if (_imageFile == null)
                    Positioned(
                      bottom: 30,
                      left: MediaQuery.of(context).size.width / 2 - 35,
                      child: Container(
                        width: 60,
                        height: 60,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: Color(0xFFF2E5D7),
                        ),
                        child: IconButton(
                          icon: Icon(Icons.camera_alt,
                              color: Color(0xFF182A3F), size: 35),
                          onPressed: _takePicture,
                        ),
                      ),
                    ),
                  if (_imageFile == null)
                    Positioned(
                      bottom: 30,
                      left: 20,
                      child: Container(
                        width: 60,
                        height: 60,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: Color(0xFFF2E5D7),
                        ),
                        child: IconButton(
                          icon: Icon(Icons.add_photo_alternate,
                              color: Color(0xFF182A3F), size: 35),
                          onPressed: _pickPictureFromGallery,
                        ),
                      ),
                    ),
                  if (_imageFile != null)
                    Positioned(
                      bottom: 30,
                      left: 20,
                      child: GestureDetector(
                        onTap: _discardPicture,
                        child: Container(
                          width: 60,
                          height: 60,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: Color(0xFFF2E5D7),
                          ),
                          child: Icon(Icons.refresh,
                              color: Color(0xFF182A3F), size: 35),
                        ),
                      ),
                    ),
                  if (_imageFile != null)
                    Positioned(
                      bottom: 30,
                      right: 20,
                      child: GestureDetector(
                        onTap: _sendPicture,
                        child: Container(
                          width: 60,
                          height: 60,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: Color(0xFFF2E5D7),
                          ),
                          padding: EdgeInsets.only(bottom: 6),
                          child: Icon(Icons.ios_share,
                              color: Color(0xFF182A3F), size: 35),
                        ),
                      ),
                    ),
                  if (_imageFile != null && _showWebView)
                    Positioned(
                      bottom: 30,
                      right: 20,
                      child: GestureDetector(
                        onTap: _goBack,
                        child: Container(
                          width: 60,
                          height: 60,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: Color(0xFFF2E5D7),
                          ),
                          child: Icon(Icons.arrow_back,
                              color: Color(0xFF182A3F), size: 35),
                        ),
                      ),
                    ),
                ],
              ),
      ),
    );
  }
}
