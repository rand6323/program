VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} UserForm1 
   Caption         =   "UserForm1"
   ClientHeight    =   3036
   ClientLeft      =   108
   ClientTop       =   456
   ClientWidth     =   4584
   OleObjectBlob   =   "UserForm1.frx":0000
   StartUpPosition =   1  '�I�[�i�[ �t�H�[���̒���
End
Attribute VB_Name = "UserForm1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Dim playerRow As Long, playerCol As Long
Dim linechk() As Long
Dim maxRow As Long, maxCol As Long
Dim goalRow As Long, goalCol As Long
Dim moveCount As Long
Dim gameOver As Boolean

Private Sub TextBox1_Change()

End Sub

Private Sub UserForm_Layout()
    
    Static fSetModal As Boolean
    If Not fSetModal Then
        
        fSetModal = True
        Me.Hide
        Me.Show vbModeless
        
    End If
    
End Sub

Private Sub UserForm_QueryClose(Cancel As Integer, CloseMode As Integer)

    Dim ws1 As Worksheet
    Dim ws2 As Worksheet
    
    Set ws1 = Worksheets("settings")
    Set ws2 = Worksheets("meiro")
    
    ' �O��̃v���C���[�ʒu�́u���v������
    If playerRow >= 1 And playerCol >= 1 Then
        ws2.Cells(playerRow, playerCol).Value = ""
        
        If ws2.Cells(maxRow, maxCol).Value <> "G" Then
            
            ws2.Cells(maxRow, maxCol).Value = "G"
            
        End If
        
        ws2.Cells(1, 1).Value = "S"
        ws1.Activate
        
    End If
    
    Unload Me
    
End Sub

Private Sub UserForm_Initialize()
    Dim ws1 As Worksheet, ws2 As Worksheet
    Dim i As Long, j As Long
    Dim bod As Borders
    
    gameOver = False
    moveCount = 0
    lblMoveCount.Caption = "�ړ���: 0"
    
    Set ws1 = Worksheets("settings")
    Set ws2 = Worksheets("meiro")
    
    maxRow = ws1.Cells(1, 2)
    maxCol = ws1.Cells(2, 2)
    
    goalRow = maxRow
    goalCol = maxCol
    
    ReDim linechk(1 To maxRow, 1 To maxCol, 0 To 3)
    
    ' linechk�Ɍr�������擾
    For i = 1 To maxRow
        For j = 1 To maxCol
            Set bod = ws2.Cells(i, j).Borders
            linechk(i, j, 0) = bod(7).LineStyle ' ��
            linechk(i, j, 1) = bod(8).LineStyle ' ��
            linechk(i, j, 2) = bod(9).LineStyle ' ��
            linechk(i, j, 3) = bod(10).LineStyle ' �E
        Next j
    Next i
    
    ' �����ʒu
    playerRow = 1
    playerCol = 1
    ws2.Cells(playerRow, playerCol).Value = "��"
    
    txtKey.SetFocus
    
End Sub

Private Sub txtKey_KeyDown(ByVal KeyCode As MSForms.ReturnInteger, ByVal Shift As Integer)
    Dim newRow As Long, newCol As Long
    Dim ws2 As Worksheet
    Set ws2 = Worksheets("meiro")

    Select Case KeyCode
        Case vbKeyUp
            If linechk(playerRow, playerCol, 1) = xlLineStyleNone Then
                MovePlayer -1, 0
            End If
        Case vbKeyDown
            If linechk(playerRow, playerCol, 2) = xlLineStyleNone Then
                MovePlayer 1, 0
            End If
        Case vbKeyLeft
            If linechk(playerRow, playerCol, 0) = xlLineStyleNone Then
                MovePlayer 0, -1
            End If
        Case vbKeyRight
            If linechk(playerRow, playerCol, 3) = xlLineStyleNone Then
                MovePlayer 0, 1
            End If
    End Select
    txtKey.SetFocus
End Sub

Private Sub MovePlayer(ByVal dr As Long, ByVal dc As Long)

    If gameOver Then Exit Sub  ' �S�[�������瑀��֎~
    
    Dim ws2 As Worksheet
    Set ws2 = Worksheets("meiro")

    Dim newRow As Long, newCol As Long
    newRow = playerRow + dr
    newCol = playerCol + dc

    If newRow < 1 Or newRow > maxRow Or newCol < 1 Or newCol > maxCol Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' ���݈ʒu���N���A
    ws2.Cells(playerRow, playerCol).Value = ""
    
    ' �V�����ʒu�Ɉړ�
    playerRow = newRow
    playerCol = newCol
    ws2.Cells(playerRow, playerCol).Value = "��"

    ' �X�N���[���ʒu���v���C���[�ɍ��킹��
    
    Dim win As Window
    Set win = ws2.Parent.Windows(1)
    
    Const MARGIN_ROWS As Long = 20 ' �㉺��5�s�̗]�T
    Const MARGIN_COLS As Long = 50 ' ���E��3��̗]�T
    
    With win
        ' ��[�ɋ߂��Ȃ��ɃX�N���[��
        If playerRow < .ScrollRow + MARGIN_ROWS Then
            .ScrollRow = Application.Max(1, playerRow - MARGIN_ROWS)
        End If
        ' ���[�ɋ߂��Ȃ牺�ɃX�N���[��
        If playerRow > .ScrollRow + .VisibleRange.Rows.Count - MARGIN_ROWS Then
            .ScrollRow = playerRow - .VisibleRange.Rows.Count + MARGIN_ROWS
        End If

        ' ���[�ɋ߂��Ȃ獶�ɃX�N���[��
        If playerCol < .ScrollColumn + MARGIN_COLS Then
            .ScrollColumn = Application.Max(1, playerCol - MARGIN_COLS)
        End If
        ' �E�[�ɋ߂��Ȃ�E�ɃX�N���[��
        If playerCol > .ScrollColumn + .VisibleRange.Columns.Count - MARGIN_COLS Then
            .ScrollColumn = playerCol - .VisibleRange.Columns.Count + MARGIN_COLS
        End If
    End With
    
    ' �ړ�������
    moveCount = moveCount + 1
    lblMoveCount.Caption = "�ړ���: " & moveCount
    
    Application.ScreenUpdating = True
    
    If playerRow = goalRow And playerCol = goalCol Then
        gameOver = True
        MsgBox "�S�[���I"
    End If
    
End Sub

Private Sub btnReset_Click()
    Call UserForm_Initialize ' �܂��̓��Z�b�g�p�̕ʏ������쐬���ČĂ�
End Sub
