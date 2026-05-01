import 'dotenv/config';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.NVIDIA_API_KEY,
  baseURL: 'https://integrate.api.nvidia.com/v1',
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: 'mistralai/mixtral-8x7b-instruct-v0.1',
    messages: [{ role: 'user', content: 'Hello from the NVIDIA API via OpenAI client!' }],
    temperature: 0.5,
    top_p: 1,
    max_tokens: 1024,
    stream: true,
  });

  for await (const chunk of completion) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
