param(
    [Parameter(Mandatory=$true)][string]$Rev,
    [Parameter(Mandatory=$true)][string]$Actor,
    [Parameter(Mandatory=$true)][string]$Branch
)

Write-Host "Creating revision $Rev by $Actor on branch $Branch"

$branchSafe = $Branch -replace '[^A-Za-z0-9_]', '_'
$dir = Join-Path "vcs_changes" $branchSafe
New-Item -ItemType Directory -Force $dir | Out-Null

$revUpper = $Rev.ToUpper()
$className = "Revision_${revUpper}_${branchSafe}"
$filePath = Join-Path $dir "$className.java"

$content = @"
public class $className {
    public static final String REVISION = "$Rev";
    public static final String AUTHOR = "$Actor";
    public static final String BRANCH = "$Branch";

    public static String info() {
        return REVISION + " by " + AUTHOR + " on " + BRANCH;
    }
}
"@

Set-Content -Path $filePath -Value $content -Encoding UTF8

git add .
git commit -m "${Rev}: ${Actor} change on ${Branch}"
git tag $Rev

Write-Host "Revision $Rev created"
