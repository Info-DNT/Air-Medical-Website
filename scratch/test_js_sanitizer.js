// Simulating window and function
const sanitize24X7 = function(text) {
  if (!text || typeof text !== "string") return text;
  try {
    const regex = new RegExp("(?<!airmedical)(?<!airmedical-)(?<!airmedical_)(24/7|24[xX]7)", "gi");
    return text.replace(regex, "24X7");
  } catch (e) {
    // Fallback if lookbehind is not supported
    let temp = text;
    const placeholders = [];
    temp = temp.replace(/airmedical[-_]?24[xX]7/gi, (match) => {
      placeholders.push(match);
      return `__AIRMED_PLACEHOLDER_${placeholders.length - 1}__`;
    });
    temp = temp.replace(/(24\/7|24[xX]7)/gi, "24X7");
    temp = temp.replace(/__AIRMED_PLACEHOLDER_(\d+)__/g, (match, idx) => {
      return placeholders[parseInt(idx)];
    });
    return temp;
  }
};

const fallbackSanitize24X7 = function(text) {
  if (!text || typeof text !== "string") return text;
  let temp = text;
  const placeholders = [];
  temp = temp.replace(/airmedical[-_]?24[xX]7/gi, (match) => {
    placeholders.push(match);
    return `__AIRMED_PLACEHOLDER_${placeholders.length - 1}__`;
  });
  temp = temp.replace(/(24\/7|24[xX]7)/gi, "24X7");
  temp = temp.replace(/__AIRMED_PLACEHOLDER_(\d+)__/g, (match, idx) => {
    return placeholders[parseInt(idx)];
  });
  return temp;
};

const testCases = [
  {
    input: "Air Medical 24x7 Team is here 24/7.",
    expected: "Air Medical 24X7 Team is here 24X7."
  },
  {
    input: "Our website is airmedical24x7.com and email info@airmedical24x7.com.",
    expected: "Our website is airmedical24x7.com and email info@airmedical24x7.com."
  },
  {
    input: "Visit https://airmedical-24x7.com/about-us for 24/7 support.",
    expected: "Visit https://airmedical-24x7.com/about-us for 24X7 support."
  },
  {
    input: "Contact us at info@airmedical24x7.com.",
    expected: "Contact us at info@airmedical24x7.com."
  },
  {
    input: "Air Medical 24X7 offers 24x7 service.",
    expected: "Air Medical 24X7 offers 24X7 service."
  }
];

console.log("Testing primary lookbehind-based sanitizer:");
let passedMain = true;
for (const tc of testCases) {
  const result = sanitize24X7(tc.input);
  if (result === tc.expected) {
    console.log(`[PASS] "${tc.input}" -> "${result}"`);
  } else {
    console.log(`[FAIL] "${tc.input}"\n  Expected: "${tc.expected}"\n  Got:      "${result}"`);
    passedMain = false;
  }
}

console.log("\nTesting fallback placeholder-based sanitizer:");
let passedFallback = true;
for (const tc of testCases) {
  const result = fallbackSanitize24X7(tc.input);
  if (result === tc.expected) {
    console.log(`[PASS] "${tc.input}" -> "${result}"`);
  } else {
    console.log(`[FAIL] "${tc.input}"\n  Expected: "${tc.expected}"\n  Got:      "${result}"`);
    passedFallback = false;
  }
}

if (passedMain && passedFallback) {
  console.log("\nAll tests passed successfully! Clean integration verified.");
  process.exit(0);
} else {
  console.log("\nSome tests failed.");
  process.exit(1);
}
