import React, { useState } from 'react';

type TestType = '単体テスト' | '結合テスト' | 'システムテスト';

interface TestCase {
  id: string;
  testType: TestType;
  title: string;
  description: string;
  expectedResult: string;
  targetFile: string;
}

const TestCaseCreator: React.FC = () => {
  const [testCase, setTestCase] = useState<TestCase>({
    id: '',
    testType: '単体テスト',
    title: '',
    description: '',
    expectedResult: '',
    targetFile: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // テストケースの保存処理をここに実装
    console.log('保存されたテストケース:', testCase);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">テストケース作成</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-2">テスト種類:</label>
          <select
            value={testCase.testType}
            onChange={(e) => setTestCase({...testCase, testType: e.target.value as TestType})}
            className="w-full p-2 border rounded"
          >
            <option value="単体テスト">単体テスト</option>
            <option value="結合テスト">結合テスト</option>
            <option value="システムテスト">システムテスト</option>
          </select>
        </div>

        <div>
          <label className="block mb-2">対象ファイル:</label>
          <input
            type="text"
            value={testCase.targetFile}
            onChange={(e) => setTestCase({...testCase, targetFile: e.target.value})}
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block mb-2">テストケースタイトル:</label>
          <input
            type="text"
            value={testCase.title}
            onChange={(e) => setTestCase({...testCase, title: e.target.value})}
            className="w-full p-2 border rounded"
          />
        </div>

        <div>
          <label className="block mb-2">テスト内容:</label>
          <textarea
            value={testCase.description}
            onChange={(e) => setTestCase({...testCase, description: e.target.value})}
            className="w-full p-2 border rounded h-32"
          />
        </div>

        <div>
          <label className="block mb-2">期待結果:</label>
          <textarea
            value={testCase.expectedResult}
            onChange={(e) => setTestCase({...testCase, expectedResult: e.target.value})}
            className="w-full p-2 border rounded h-32"
          />
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          保存
        </button>
      </form>
    </div>
  );
};

export default TestCaseCreator;
