Attribute VB_Name = "Module1"
Option Explicit

Public playerRow As Long
Public playerCol As Long
Public linechk() As Long

Sub onScreen(ByVal judScreen As Boolean)
    
    If judScreen = False Then
        
        Application.ScreenUpdating = False
        Application.EnableEvents = False
        Application.Calculation = xlCalculationManual
    
    Else
        
        Application.EnableEvents = True
        Application.Calculation = xlCalculationAutomatic
        Application.ScreenUpdating = True
    
    End If
    
End Sub

Function meiroReady() As Boolean
    
    Dim ws2 As Worksheet
    Dim maxRow As Long, maxCol As Long
    Set ws2 = Worksheets("meiro")
    
    maxRow = Worksheets("settings").Cells(1, 2).Value
    maxCol = Worksheets("settings").Cells(2, 2).Value
    
    meiroReady = (ws2.Cells(maxRow, maxCol).Value = "G")
    
End Function

Sub meiroPlay()
    
    If meiroReady() = False Then
        MsgBox "迷路がまだ作成されていません！"
        Exit Sub
    End If
    
    Dim ws2 As Worksheet
    Set ws2 = Worksheets("meiro")
    
    ws2.Activate
    ws2.Range("A1").Select
    UserForm1.Show
    
End Sub

Sub StageGenerate(ByVal MAX_SIZE_ROW As Long, ByVal MAX_SIZE_COL As Long)
    
    Dim i As Long, j As Long
    Dim jud As Long
    Dim c1 As Long
    Dim row As Long, col As Long
    Dim row_e As Long, col_e As Long
    Dim cnt As Long
    
    Dim ws2 As Worksheet
    Dim lineRange As Range
    Dim MAX_SIZE_RC2 As Long
    
    Set ws2 = Worksheets("meiro")
    MAX_SIZE_RC2 = MAX_SIZE_ROW + MAX_SIZE_COL
    
    Call onScreen(False)
    
    'セルが通過したかどうかを判別する
    '0→通ってない
    '1→通過済み
    '2→行き止まり
    ReDim stageData(MAX_SIZE_ROW + 2, MAX_SIZE_COL + 2) As Long
    
    '迷路を作る範囲を指定
    Set lineRange = ws2.Range(ws2.Cells(1, 1), ws2.Cells(MAX_SIZE_ROW, MAX_SIZE_COL))
    
    ws2.Cells.Clear
    lineRange.Borders.LineStyle = True
    
    
    '行き止まりマスを判別
    For i = 0 To MAX_SIZE_ROW + 1
        
        stageData(i, 0) = 2
        stageData(i, MAX_SIZE_COL + 1) = 2
        
        For j = 0 To MAX_SIZE_COL + 1
        
            stageData(0, j) = 2
            stageData(MAX_SIZE_ROW + 1, j) = 2
            
        Next
    Next
    
    row = Int(Rnd() * (MAX_SIZE_ROW - 1)) + 1
    col = Int(Rnd() * (MAX_SIZE_COL - 1)) + 1
    
    '始点となるマスなので、通過済みとする
    stageData(row, col) = 1
    
    cnt = MAX_SIZE_ROW * MAX_SIZE_COL - 1
    
    '通過していないマスを通ると、cntが1減る
    'これをcntが0になるまで続ける
    Do
        
        '罫線の削除位置を乱数を発生させ、指定する
        '後述のBorders()の引数は以下のとおり
        ' 7＝xlEdgeLeft(左側)
        ' 8＝xlEdgeTop(上側)
        ' 9＝xlEdgeBottom(下側)
        '10＝xlEdgeRight(右側)
        '例えば左側の場合、rowは0、colは-1
        jud = Int(Rnd() * 4)
        c1 = 2 * jud - 3
        row_e = row + c1 Mod 3
        col_e = col + c1 \ 3
        
        '通過していないマスの罫線を削除する(位置は先ほど指定済み)
        'stageDataに1を代入して通過済みとし、
        '移動(位置の更新)を行い、cntを1減らす
        If stageData(row_e, col_e) = 0 Then
            
            lineRange(row, col).Borders(7 + jud).LineStyle = xlLineStyleNone
            stageData(row_e, col_e) = 1
            row = row_e
            col = col_e
            cnt = cnt - 1
        
        '通過済みマスなので、移動(位置の更新)だけ行う
        ElseIf stageData(row_e, col_e) = 1 Then
            
            row = row_e
            col = col_e
            
            
        '行き止まりのときは、移動しない
        End If
        
    Loop Until cnt = 0
    
    Erase stageData
    lineRange.BorderAround Weight:=xlMedium
    
    'それぞれSTARTのSと、GOALのG
    'スタート地点とゴール地点をハッキリとさせておく
    ws2.Cells(1, 1) = "S"
    ws2.Cells(MAX_SIZE_ROW, MAX_SIZE_COL) = "G"
    
    Call onScreen(True)
    
End Sub

Sub meiroArea()
    
    Randomize
    
    Dim ws1 As Worksheet
    
    Set ws1 = Worksheets("settings")
    Call StageGenerate(ws1.Cells(1, 2), ws1.Cells(2, 2))
    
End Sub

Sub meiroDelete()
    
    Dim ws1 As Worksheet
    Dim ws2 As Worksheet
    
    Set ws1 = Worksheets("settings")
    Set ws2 = Worksheets("meiro")
    
    Application.ScreenUpdating = False
    
    ws2.Activate
    ws2.Range("A1").Select
    ws2.Cells.Clear
    ws1.Activate
    
    Application.ScreenUpdating = True
    
End Sub
