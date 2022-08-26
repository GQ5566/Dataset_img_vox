import vtk

input1 = vtk.vtkPolyData()
reader1 = vtk.vtkSTLReader()
reader1.SetFileName(r"E:\document\learning\thesis\Master thesis\python\projections\p_1.stl")
reader1.Update()
input1 = reader1.GetOutput()  # 读取模型A

input2 = vtk.vtkPolyData()
reader2 = vtk.vtkSTLReader()
reader2.SetFileName(r"E:\document\learning\thesis\Master thesis\python\projections\p_1.stl")
reader2.Update()
input2 = reader2.GetOutput()  # 读取模型B


# 数据合并，可以合并显示两个模型
clean1 = vtk.vtkCleanPolyData()
clean1.SetInputData(input1)

clean2 = vtk.vtkCleanPolyData()
clean2.SetInputData(input2)

distanceFilter = vtk.vtkDistancePolyDataFilter()

distanceFilter.SetInputConnection(1, clean1.GetOutputPort())
distanceFilter.SetInputConnection(0, clean2.GetOutputPort())
distanceFilter.SignedDistanceOff()
distanceFilter.Update()  # 计算距离
distanceFilter.GetOutputPort()
mapper = vtk.vtkPolyDataMapper()  # 配置mapper
mapper.SetInputConnection(distanceFilter.GetOutputPort())
mapper.SetScalarRange(  # 设置颜色映射范围
  distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[0],
  distanceFilter.GetOutput().GetPointData().GetScalars().GetRange()[1])
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor1 = vtk.vtkActor()
actor1.SetMapper(mapper)
lut = vtk.vtkLookupTable()
lut.SetHueRange(0.2, 0.7)  # 映射的颜色变换参数（自己调颜色）
# lut.SetAlphaRange(1.0, 1.0)
# lut.SetValueRange(1.0, 1.0)
# lut.SetSaturationRange(1.0, 1.0)
# lut.SetNumberOfTableValues(256)
mapper.SetLookupTable(lut)
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInputData((distanceFilter.GetSecondDistanceOutput()))
mapper2.SetScalarRange(  # 设置颜色映射范围
  distanceFilter.GetSecondDistanceOutput().GetPointData().GetScalars().GetRange()[0],
  distanceFilter.GetSecondDistanceOutput().GetPointData().GetScalars().GetRange()[1])


actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)

scalarBar = vtk.vtkScalarBarActor()  # 设置color_bar
scalarBar.SetLookupTable(mapper.GetLookupTable())
scalarBar.SetTitle("SD(mm)")
scalarBar.SetNumberOfLabels(5)  # 设置要显示的刻度标签数。自己设定色带的位置
scalarBar.SetMaximumNumberOfColors(10)
# scalarBar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
# scalarBar.GetPositionCoordinate().SetValue(0.01, 0.49)  # 参数越小越靠左，第二个参数越大越往上
# scalarBar.SetWidth(0.16)
# scalarBar.SetHeight(0.5)
# scalarBar.SetTextPositionToPrecedeScalarBar()  # 标题和刻度标记是否应在标量栏之前(文字会出现在条形左边)
# # 设置标题和条形之间的边距
# scalarBar.SetVerticalTitleSeparation(10)
# # 设置标题颜色
scalarBar.DrawTickLabelsOn()
scalarBar.GetTitleTextProperty().SetColor(0, 0, 0)
scalarBar.GetLabelTextProperty().SetColor(0, 0, 0)
arender = vtk.vtkRenderer()
arender.SetViewport(0, 0.0, 1, 1.0)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(arender)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
style = vtk.vtkInteractorStyleTrackballActor()
iren.SetInteractorStyle(style)
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, -1, 0)
aCamera.ComputeViewPlaneNormal()
aCamera.Azimuth(30.0)
aCamera.Elevation(30.0)
aCamera.Dolly(1.5)

arender.AddActor(actor)
# arender.AddActor(actor1)
arender.SetActiveCamera(aCamera)
arender.ResetCamera()
arender.SetBackground(1, 1, 1)
arender.ResetCameraClippingRange()
arender.AddActor2D(scalarBar)

renWin.Render()
iren.Initialize()
iren.Start()