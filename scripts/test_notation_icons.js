const fs = require('fs');

const js = fs.readFileSync('frontend/assets/js/app.js', 'utf8');

// Extract the notation engine functions block
const startIdx = js.indexOf('const COMMAND_DIR_SVGS =');
const endIdx = js.indexOf('function setControllerLayout');

if (startIdx === -1 || endIdx === -1) {
  console.error('Could not find notation engine block in app.js');
  process.exit(1);
}

const engineCode = js.slice(startIdx, endIdx);

// Minimal sandbox
const state = { controllerLayout: 'ARCADE' };
const window = {};

const vm = require('vm');
const ctx = vm.createContext({
  console,
  state,
  window,
  COMMAND_DIR_SVGS: null,
  renderCommandNotation: null
});

vm.runInContext(engineCode, ctx);

const renderCommandNotation = ctx.renderCommandNotation;

const testCases = [
  { input: 'df+2', expectIcons: ['df.svg', '2.svg'] },
  { input: 'f,n,d,df+2', expectIcons: ['f.svg', 'n.svg', 'd.svg', 'df.svg', '2.svg'] },
  { input: '1,2', expectIcons: ['1.svg', '2.svg'] },
  { input: '1+2', expectIcons: ['1+2.svg'] },
  { input: '3+4', expectIcons: ['3+4.svg'] },
  { input: '1+2+3+4', expectIcons: ['1+2+3+4.svg'] },
  { input: 'f,f+3', expectIcons: ['f.svg', '3.svg'] },
  { input: 'qcf+1', expectIcons: ['d.svg', 'df.svg', 'f.svg', '1.svg'] },
  { input: 'df+2 > 4 > (T!) > f,f,f+2+4', expectIcons: ['df.svg', '2.svg', 'follow.svg', '4.svg', 'tornado.svg', 'f.svg', '2+4.svg'] },
  { input: 'H.2+3', expectIcons: ['heat.svg', '2+3.svg'] },
  { input: 'R.1+2', expectIcons: ['rage-art.svg', '1+2.svg'] }
];

let allPassed = true;

testCases.forEach(({ input, expectIcons }) => {
  const output = renderCommandNotation(input, 'ARCADE');
  let tcPassed = true;
  for (const icon of expectIcons) {
    if (!output.includes(icon)) {
      console.error(`FAIL: '${input}' missing expected icon '${icon}'`);
      tcPassed = false;
      allPassed = false;
    }
  }
  if (tcPassed) {
    console.log(`PASS: '${input}' properly rendered with all expected icons: ${expectIcons.join(', ')}`);
  }
});

// Also test PS and Xbox layouts
const psOutput = renderCommandNotation('1+2', 'PLAYSTATION');
if (psOutput.includes('ps-square.svg') && psOutput.includes('ps-triangle.svg')) {
  console.log('PASS: PlayStation layout rendered ps-square.svg and ps-triangle.svg');
} else {
  console.error('FAIL: PlayStation layout missing ps icons');
  allPassed = false;
}

const xbOutput = renderCommandNotation('1+2', 'XBOX');
if (xbOutput.includes('xb-x.svg') && xbOutput.includes('xb-y.svg')) {
  console.log('PASS: Xbox layout rendered xb-x.svg and xb-y.svg');
} else {
  console.error('FAIL: Xbox layout missing xb icons');
  allPassed = false;
}

if (!allPassed) {
  process.exit(1);
} else {
  console.log('\nALL NOTATION ICON TESTS PASSED PERFECTLY WITH ZERO ERRORS!');
}
