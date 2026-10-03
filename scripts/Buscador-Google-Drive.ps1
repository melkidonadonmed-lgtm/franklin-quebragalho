# Buscador Nativo Google Drive • Franklin Quebra-Galho
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$jsonPath = "C:\Users\melki\.gemini\antigravity\brain\c000597e-53fb-4675-a6dd-8a23a33fa94d\scratch\drive_data_full.json"
if (-not (Test-Path $jsonPath)) {
    [System.Windows.Forms.MessageBox]::Show("Base de dados de busca não encontrada.", "Google Drive Explorer", 0, 16)
    exit
}

$jsonData = Get-Content -LiteralPath $jsonPath -Raw -Encoding utf8 | ConvertFrom-Json
$allFiles = [System.Collections.Generic.List[PSCustomObject]]::new()

foreach ($root in $jsonData) {
    foreach ($f in $root.Folders) {
        if ($f.DirectFiles) {
            foreach ($file in $f.DirectFiles) {
                $allFiles.Add([PSCustomObject]@{
                    Nome = $file.n
                    Tipo = $file.e
                    Tamanho = "$($file.s) KB"
                    Data = $file.m
                    Pasta = $f.FullPath
                    PastaNome = $f.Name
                })
            }
        }
    }
}

# Criar Janela Principal
$form = New-Object System.Windows.Forms.Form
$form.Text = "Buscador do Google Drive • Franklin Quebra-Galho"
$form.Size = New-Object System.Drawing.Size(960, 620)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(15, 23, 42)
$form.ForeColor = [System.Drawing.Color]::FromArgb(248, 250, 252)
$form.Font = New-Object System.Drawing.Font("Segoe UI", 9.5)

# Barra Superior com Atalhos
$topPanel = New-Object System.Windows.Forms.Panel
$topPanel.Dock = "Top"
$topPanel.Height = 105
$topPanel.BackColor = [System.Drawing.Color]::FromArgb(30, 41, 59)
$form.Controls.Add($topPanel)

# Botões de Atalho Rápido para o Internato
$btnModelos = New-Object System.Windows.Forms.Button
$btnModelos.Text = "⚡ 01 - Modelos Rápidos (Internato)"
$btnModelos.Location = New-Object System.Drawing.Point(16, 12)
$btnModelos.Size = New-Object System.Drawing.Size(260, 34)
$btnModelos.BackColor = [System.Drawing.Color]::FromArgb(56, 189, 248)
$btnModelos.ForeColor = [System.Drawing.Color]::FromArgb(15, 23, 42)
$btnModelos.FlatStyle = "Flat"
$btnModelos.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$btnModelos.Cursor = [System.Windows.Forms.Cursors]::Hand
$btnModelos.Add_Click({
    Start-Process "explorer.exe" "G:\Meu Drive\01_Modelos_Rapidos"
})
$topPanel.Controls.Add($btnModelos)

$btnProt = New-Object System.Windows.Forms.Button
$btnProt.Text = "💊 02 - Protocolos e Remédios"
$btnProt.Location = New-Object System.Drawing.Point(286, 12)
$btnProt.Size = New-Object System.Drawing.Size(230, 34)
$btnProt.BackColor = [System.Drawing.Color]::FromArgb(16, 185, 129)
$btnProt.ForeColor = [System.Drawing.Color]::FromArgb(15, 23, 42)
$btnProt.FlatStyle = "Flat"
$btnProt.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$btnProt.Cursor = [System.Windows.Forms.Cursors]::Hand
$btnProt.Add_Click({
    Start-Process "explorer.exe" "G:\Meu Drive\02_Protocolos_e_Medicamentos"
})
$topPanel.Controls.Add($btnProt)

$btnMed = New-Object System.Windows.Forms.Button
$btnMed.Text = "🩺 03 - Medicina Faculdade"
$btnMed.Location = New-Object System.Drawing.Point(526, 12)
$btnMed.Size = New-Object System.Drawing.Size(210, 34)
$btnMed.BackColor = [System.Drawing.Color]::FromArgb(99, 102, 241)
$btnMed.ForeColor = [System.Drawing.Color]::White
$btnMed.FlatStyle = "Flat"
$btnMed.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$btnMed.Cursor = [System.Windows.Forms.Cursors]::Hand
$btnMed.Add_Click({
    Start-Process "explorer.exe" "G:\Meu Drive\01_Medicina_Faculdade"
})
$topPanel.Controls.Add($btnMed)

$btnDrive = New-Object System.Windows.Forms.Button
$btnDrive.Text = "☁️ Raiz G:\"
$btnDrive.Location = New-Object System.Drawing.Point(746, 12)
$btnDrive.Size = New-Object System.Drawing.Size(120, 34)
$btnDrive.BackColor = [System.Drawing.Color]::FromArgb(71, 85, 105)
$btnDrive.ForeColor = [System.Drawing.Color]::White
$btnDrive.FlatStyle = "Flat"
$btnDrive.Cursor = [System.Windows.Forms.Cursors]::Hand
$btnDrive.Add_Click({
    Start-Process "explorer.exe" "G:\Meu Drive"
})
$topPanel.Controls.Add($btnDrive)

# Caixa de Busca
$lblBusca = New-Object System.Windows.Forms.Label
$lblBusca.Text = "🔍 Buscar:"
$lblBusca.Location = New-Object System.Drawing.Point(16, 62)
$lblBusca.Size = New-Object System.Drawing.Size(80, 24)
$lblBusca.ForeColor = [System.Drawing.Color]::FromArgb(148, 163, 184)
$topPanel.Controls.Add($lblBusca)

$txtBusca = New-Object System.Windows.Forms.TextBox
$txtBusca.Location = New-Object System.Drawing.Point(95, 60)
$txtBusca.Size = New-Object System.Drawing.Size(580, 26)
$txtBusca.BackColor = [System.Drawing.Color]::FromArgb(15, 23, 42)
$txtBusca.ForeColor = [System.Drawing.Color]::White
$txtBusca.BorderStyle = "FixedSingle"
$topPanel.Controls.Add($txtBusca)

$lblStatus = New-Object System.Windows.Forms.Label
$lblStatus.Text = "5.686 arquivos indexados"
$lblStatus.Location = New-Object System.Drawing.Point(690, 62)
$lblStatus.Size = New-Object System.Drawing.Size(230, 24)
$lblStatus.ForeColor = [System.Drawing.Color]::FromArgb(56, 189, 248)
$topPanel.Controls.Add($lblStatus)

# Tabela ListView
$listView = New-Object System.Windows.Forms.ListView
$listView.Dock = "Fill"
$listView.View = "Details"
$listView.FullRowSelect = $true
$listView.GridLines = $true
$listView.BackColor = [System.Drawing.Color]::FromArgb(15, 23, 42)
$listView.ForeColor = [System.Drawing.Color]::FromArgb(248, 250, 252)
$listView.BorderStyle = "None"

$listView.Columns.Add("Nome do Arquivo", 400) | Out-Null
$listView.Columns.Add("Tipo", 70) | Out-Null
$listView.Columns.Add("Tamanho", 90) | Out-Null
$listView.Columns.Add("Data", 90) | Out-Null
$listView.Columns.Add("Pasta de Origem", 280) | Out-Null

$form.Controls.Add($listView)

# Barra Inferior com Ações
$bottomPanel = New-Object System.Windows.Forms.Panel
$bottomPanel.Dock = "Bottom"
$bottomPanel.Height = 52
$bottomPanel.BackColor = [System.Drawing.Color]::FromArgb(30, 41, 59)
$form.Controls.Add($bottomPanel)

$btnAbrirPasta = New-Object System.Windows.Forms.Button
$btnAbrirPasta.Text = "📂 Abrir no Windows Explorer"
$btnAbrirPasta.Location = New-Object System.Drawing.Point(16, 10)
$btnAbrirPasta.Size = New-Object System.Drawing.Size(240, 32)
$btnAbrirPasta.BackColor = [System.Drawing.Color]::FromArgb(56, 189, 248)
$btnAbrirPasta.ForeColor = [System.Drawing.Color]::FromArgb(15, 23, 42)
$btnAbrirPasta.FlatStyle = "Flat"
$btnAbrirPasta.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$btnAbrirPasta.Cursor = [System.Windows.Forms.Cursors]::Hand
$bottomPanel.Controls.Add($btnAbrirPasta)

$btnCopiar = New-Object System.Windows.Forms.Button
$btnCopiar.Text = "📋 Copiar Caminho"
$btnCopiar.Location = New-Object System.Drawing.Point(268, 10)
$btnCopiar.Size = New-Object System.Drawing.Size(150, 32)
$btnCopiar.BackColor = [System.Drawing.Color]::FromArgb(71, 85, 105)
$btnCopiar.ForeColor = [System.Drawing.Color]::White
$btnCopiar.FlatStyle = "Flat"
$btnCopiar.Cursor = [System.Windows.Forms.Cursors]::Hand
$bottomPanel.Controls.Add($btnCopiar)

$lblHint = New-Object System.Windows.Forms.Label
$lblHint.Text = "💡 Dê 2 cliques em qualquer item para abrir a pasta imediatamente no Explorer!"
$lblHint.Location = New-Object System.Drawing.Point(435, 16)
$lblHint.Size = New-Object System.Drawing.Size(500, 24)
$lblHint.ForeColor = [System.Drawing.Color]::FromArgb(148, 163, 184)
$bottomPanel.Controls.Add($lblHint)

# Função de preenchimento e busca rápida
$populateList = {
    param($term)
    $listView.BeginUpdate()
    $listView.Items.Clear()
    
    $results = if ([string]::IsNullOrWhiteSpace($term)) {
        $allFiles | Select-Object -First 100
    } else {
        $termLower = $term.ToLower().Trim()
        $allFiles | Where-Object { $_.Nome.ToLower().Contains($termLower) -or $_.Pasta.ToLower().Contains($termLower) } | Select-Object -First 250
    }
    
    foreach ($item in $results) {
        $lvi = New-Object System.Windows.Forms.ListViewItem($item.Nome)
        $lvi.SubItems.Add($item.Tipo) | Out-Null
        $lvi.SubItems.Add($item.Tamanho) | Out-Null
        $lvi.SubItems.Add($item.Data) | Out-Null
        $lvi.SubItems.Add($item.PastaNome) | Out-Null
        $lvi.Tag = $item.Pasta
        $listView.Items.Add($lvi) | Out-Null
    }
    
    $lblStatus.Text = "$($listView.Items.Count) exibidos de $($allFiles.Count)"
    $listView.EndUpdate()
}

$txtBusca.Add_TextChanged({
    & $populateList $txtBusca.Text
})

$actionAbrir = {
    if ($listView.SelectedItems.Count -gt 0) {
        $pasta = $listView.SelectedItems[0].Tag
        if ($pasta -and (Test-Path $pasta)) {
            Start-Process "explorer.exe" $pasta
        } else {
            [System.Windows.Forms.MessageBox]::Show("Pasta não encontrada: $pasta", "Aviso", 0, 48)
        }
    }
}

$btnAbrirPasta.Add_Click($actionAbrir)
$listView.Add_DoubleClick($actionAbrir)

$btnCopiar.Add_Click({
    if ($listView.SelectedItems.Count -gt 0) {
        $pasta = $listView.SelectedItems[0].Tag
        [System.Windows.Forms.Clipboard]::SetText($pasta)
    }
})

& $populateList ""
$form.ShowDialog() | Out-Null
