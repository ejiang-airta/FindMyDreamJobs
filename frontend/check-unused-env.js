// check-unused-env.js
const fs = require('fs')
const path = require('path')

const envFile = path.resolve(__dirname, '.env.local')
const filesToCheck = ['src', 'app', 'lib', 'components']

const envVars = fs.readFileSync(envFile, 'utf-8')
  .split('\n')
  .filter(Boolean)
  .filter(line => !line.startsWith('#'))
  .map(line => line.split('=')[0])

const codeFiles = []

function collectFiles(dir) {
  const entries = fs.readdirSync(dir)
  for (const file of entries) {
    const fullPath = path.join(dir, file)
    const stat = fs.statSync(fullPath)
    if (stat.isDirectory()) {
      collectFiles(fullPath)
    } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
      codeFiles.push(fullPath)
    }
  }
}

filesToCheck.forEach(dir => {
  if (fs.existsSync(dir)) collectFiles(dir)
})

const unused = envVars.filter(envVar => {
  return !codeFiles.some(file => {
    const content = fs.readFileSync(file, 'utf-8')
    return content.includes(envVar)
  })
})

console.log('🔍 Unused .env variables:')
if (unused.length > 0) {
  unused.forEach(v => console.log('⚠️  ', v))
} else {
  console.log('✅ None! All are in use.')
}
