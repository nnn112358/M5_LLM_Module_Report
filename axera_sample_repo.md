# axera-techのリポジトリ調査

## 目的

https://github.com/orgs/AXERA-TECH/repositories  
のリポジトリで Module-LLM(ax630c)と関係ありそうなリポジトリを調査した。

## サンプルのソースコード

### ax-samples(example/ax620e)
https://github.com/AXERA-TECH/ax-samples
https://github.com/AXERA-TECH/pulsar2-docs/releases/download/v1.9/ax-samples.zip

```
	ax_classification	ax_yolov8		ax_yolo11_seg		ax_crowdcount												
	ax_yolov5s		ax_yolov8_seg		ax_yolo11_pose		ax_rtdetr												
	ax_yolov5s_seg		ax_yolov8_pose		ax_yolox		ax_depth_anything												
	ax_yolov5_face		ax_yolov9		ax_yolo_world		ax_imgproc												
	ax_yolov6		ax_yolov10		ax_yolo_world_open_vocabulary		ax_model_info												
	ax_yolov7_tiny_face	ax_yolov10_u		ax_scrfd														
	ax_yolov7		ax_yolo11		ax_simcc_pose														
```

																
### axcl-sample	
https://github.com/AXERA-TECH/axcl-sample

```
	sample_axclrt_classification																		
	sample_axclrt_yolov5s																		
```
					
### ax620e_bsp_sdk		
https://github.com/AXERA-TECH/ax620e_bsp_sdk

``` 
	FRTDemo		sample_cipher_s		sample_gzipd_s		sample_ivps		sample_npu_classification		sample_rtc		sample_vdec		sample_venc		sample_venc		sample_vin_ivps_vo_venc
	sample_audio		sample_cmm		sample_isp_3a		sample_ivps_jenc_slice		sample_npu_classification_s		sample_rtc_s		sample_vdec_ivps_venc		sample_venc_s		sample_venc_s		sample_vin_s
	sample_audio_s		sample_cmm_s		sample_ive		sample_ivps_jenc_slice_s		sample_npu_yolov5s		sample_skel		sample_vdec_ivps_venc_s		sample_vin		sample_vin		sample_vo
	sample_avs		sample_dma		sample_ive_s		sample_ivps_s		sample_npu_yolov5s_s		sample_skel_s		sample_vdec_ivps_vo		sample_vin_ivps_skel_venc_rtsp		sample_vin_ivps_skel_venc_rtsp		sample_vo_s
	sample_avs_s		sample_dma_s		sample_ives		sample_ivps_venc		sample_pool		sample_sysmap		sample_vdec_ivps_vo_s		sample_vin_ivps_skel_venc_rtsp_s		sample_vin_ivps_skel_venc_rtsp_s		
	sample_cipher		sample_gzipd		sample_ives_s		sample_ivps_venc_s		sample_pool_s		sample_sysmap_s		sample_vdec_s		sample_vin_ivps_venc_rtsp		sample_vin_ivps_venc_rtsp		
```																
### ax-npu-kit-620e		
https://github.com/AXERA-TECH/ax-npu-kit-620e
```
	hvcfp_demo																		
```										
																			
## 学習モデルの配布場所




| |ソースコード|場所|モデル|場所|
|:----|:----|:----|:----|:----|
| ax_classification|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|〇|https://drive.google.com/drive/folders/101kKzpUoHzsXft7MqbxWxUeHMxuXzHLf|
| ax_crowdcount|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_depth_anything|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|〇|https://drive.google.com/drive/folders/1cHT7zXHLhg0UuTv4kARbscKb8MJiA-0Z|
| ax_imgproc|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_model_info|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_rtdetr|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_scrfd|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_simcc_pose|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_yolo_world|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_yolov5_face|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|△|ax650e版のモデルがGoogleDriveにある|
| ax_yolov5s|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|〇|quick_start_example|
| ax_yolov5s_seg|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|△|ax650e版のモデルがGoogleDriveにある|
| ax_yolov6|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|△|ax650e版のモデルがGoogleDriveにある|
| ax_yolov7|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|△|ax650e版のモデルがGoogleDriveにある|
| ax_yolov7_tiny_face|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|△|ax650e版のモデルがGoogleDriveにある|
| ax_yolov8|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|△|ax650e版のモデルがGoogleDriveにある|
| ax_yolov8_pose|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|△|ax650e版のモデルがGoogleDriveにある|
| ax_yolov8_seg|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
| ax_yolov9|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
|ax_yolox|〇|https://github.com/AXERA-TECH/ax-samples/tree/main/examples/ax620e|×|見当たらない|
|LLM/InternalVL|×|ソースコードがない|〇|https://drive.google.com/drive/folders/1l5tlsfU43damLJ_eKor8SGtWykqY1jIL|
|LLM/qwen2.5-corder-0.5b|×|ソースコードがない|〇|https://drive.google.com/drive/folders/14gYqz2SvpuWwoHY45M0KGOyRK4Ndo0rK|
|LLM/qwen2.5-0.5b-prefill|×|ソースコードがない|〇|https://drive.google.com/drive/folders/14gYqz2SvpuWwoHY45M0KGOyRK4Ndo0rK|
|LLM/openbuddy-1b|×|ソースコードがない|〇|https://drive.google.com/drive/folders/1pkyj4VyP9URbG5xWrIGNVKJ58QXBZ0Z2|
|ax_yolo10|×|ソースコードがない|〇|https://drive.google.com/drive/folders/1ciRJ-WdvlP02J9VXtGrJ2K-mk6pxz8RK|
|ax_yolo11|×|ソースコードがない|〇|https://drive.google.com/drive/folders/1ft-WcHucGjOe6tLUUvyEo3DgpCp1SdpN?usp=drive_link|
|ax_yolo11_pose|×|ソースコードがない|〇|https://drive.google.com/drive/folders/1xfDNmIF2cKqOyB9Wle9sOJvH3RTCCKEx|
|ax_yolo11_seg|×|ソースコードがない|〇|https://drive.google.com/drive/folders/1gyHtMj5ST1_ACVRJAEUAnAV7klya-e9y|
|ax_yolo_world_open_vocabulary|×|ソースコードがない|〇|https://drive.google.com/drive/folders/1ftY0PuJGlJh-PaBcLeWgEErkmS4IF7c-|







### GoogleDrive:ModelZoo

https://drive.google.com/drive/folders/11aRxsFqJfGXhFMlInudj3Bi8SR-08TXl  
https://x.com/qqc1989/status/1855507945989038424  

```
Classification /mobilenetv2
DepthAnything  
LLM /InternVL
LLM /OpenBuddy
LLM /Qwen
YOLO11
YOLO11-Pose
YOLO11-Seg 
YOLO_World_v2
```

### GoogleDrive:ax-samples/ax650
https://drive.google.com/drive/folders/1JY59vOFS2qxI8TkVIZ0pHfxHMfKPW5PS  

```
dinov2_small_518_precision_opt.axmodel  ppyoloe_plus_crn_m_60e_objects365.axmodel        yolov5s-face.axmodel
glpdepth_448x576.axmodel                ppyoloe_plus_crn_s_60e_objects365.axmodel        yolov5s-seg.axmodel
glpdepth_512x640.axmodel                realesrganx4.axmodel                             yolov5s.axmodel
glpdepth_640x896.axmodel                realesrganx4_npu3.axmodel                        yolov6s.axmodel
glpdepth_896x1152.axmodel               rtmdet_det.axmodel                               yolov7-tiny-face.axmodel
person_attribute_infer_sim.axmodel      scrfd_500m_bnkps_shape640x640.axmodel            yolov7-tiny.axmodel
pfld.axmodel                            segformer-b0-cityscapes-640-1280-argmax.axmodel  yolov8s-pose.axmodel
portrait_pp_humansegv2.axmodel          segformer.bo.512.ade.axmodel                     yolov8s.axmodel
ppyoloe.axmodel                         vehicle_attribute_infer_sim.axmodel              yolox.axmodel

```


