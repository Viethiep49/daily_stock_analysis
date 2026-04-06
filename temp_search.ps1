$pattern = "[\x{4e00}-\x{9fff}]"
Get-ChildItem -Path . -Recurse -Include *.js,*.ts,*.tsx,*.jsx -Exclude node_modules,.git | ForEach-Object {
    $file = $_.FullName
    $lines = Get-Content $file -ErrorAction SilentlyContinue
    $lineNumber = 0
    foreach ($line in $lines) {
        $lineNumber++
        if ($line -match $pattern) {
            Write-Output "$file -> $lineNumber : $line"
        }
    }
}
