import { createClient } from "@sanity/client";
import { readFileSync, writeFileSync } from "fs";
import { basename } from "path";

const client = createClient({
  projectId: "w486ji4p",
  dataset: "production",
  apiVersion: "2024-01-01",
  token: process.env.SANITY_TOKEN,
  useCdn: false,
});

const images = [
  { path: "images/cover.png", name: "docker-mcp-cover", alt: "Visual metaphor showing tokens being funneled through Docker container with dramatic 98.7% reduction" },
  { path: "images/section-1.png", name: "docker-mcp-token-dashboard", alt: "Dashboard displaying massive token consumption before user interaction begins" },
  { path: "images/section-2.png", name: "docker-mcp-comparison", alt: "Visual comparison of traditional upfront loading vs Docker MCP's on-demand approach" },
  { path: "images/section-3.png", name: "docker-mcp-reduction-chart", alt: "Bar chart dramatically illustrating 98.7% token reduction from 150,000 to 2,000 tokens" },
  { path: "images/section-4.png", name: "docker-mcp-data-flow", alt: "Technical diagram illustrating filtered data flow in Docker MCP versus raw data transmission" },
  { path: "images/section-5.png", name: "docker-mcp-architecture", alt: "Enterprise architecture diagram showing simplified workflow with Docker MCP" },
  { path: "images/section-6.png", name: "docker-mcp-performance", alt: "Performance dashboard displaying token reduction, speed improvements, and cost savings" },
];

async function uploadImage(imagePath: string, filename: string): Promise<any> {
  const buffer = readFileSync(imagePath);
  const asset = await client.assets.upload("image", buffer, {
    filename: `${filename}.png`,
    contentType: "image/png",
  });
  return asset;
}

async function main() {
  if (!process.env.SANITY_TOKEN) {
    console.error("❌ SANITY_TOKEN environment variable is required");
    console.log("Get a token from: https://www.sanity.io/manage/project/w486ji4p/api#tokens");
    process.exit(1);
  }

  console.log("🚀 Uploading images to Sanity...\n");

  const results: Record<string, any> = {};

  for (const img of images) {
    try {
      console.log(`📤 Uploading ${img.path}...`);
      const asset = await uploadImage(img.path, img.name);
      results[img.name] = {
        _id: asset._id,
        url: asset.url,
        alt: img.alt,
      };
      console.log(`   ✅ ${asset._id}`);
    } catch (error: any) {
      console.error(`   ❌ Failed: ${error.message}`);
    }
  }

  // Save asset manifest
  writeFileSync("sanity-assets.json", JSON.stringify(results, null, 2));
  console.log("\n✅ Asset manifest saved to sanity-assets.json");
  console.log("\nUploaded assets:");
  console.table(Object.entries(results).map(([name, data]) => ({
    name,
    id: data._id,
    url: data.url?.substring(0, 60) + "...",
  })));
}

main().catch(console.error);
