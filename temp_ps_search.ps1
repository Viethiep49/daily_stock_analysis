Get-ChildItem -Path . -Recurse -Include *.js,*.ts,*.tsx,*.jsx -Exclude node_modules,.git | ForEach-Object {
    $file = $_.FullName
    $lines = Get-Content $file -ErrorAction SilentlyContinue
    $lineNumber = 0
    foreach ($line in $lines) {
        $lineNumber++
        if ($line -match '[\u4e00-\u9fff]') {
            Write-Output "$file -> $lineNumber : $line"
        }
    }
}
