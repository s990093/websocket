import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const darkMode = true;
  const ws = new WebSocket('ws://49.213.238.75:8003/ws/chat/mouse/');

  useEffect(() => {
    // 建立 WebSocket 連接

    ws.onopen = () => {
      console.log('WebSocket 連接成功！');
    };

    ws.onerror = (error) => {
      console.error('WebSocket 錯誤發生：', error);
    };

    ws.onclose = () => {
      console.log('WebSocket 連接關閉！');
    };

    // 清理函數，用於斷開 WebSocket 連接
    return () => {
      ws.close();
    };
  }, []); // 空依賴陣列確保只執行一次

  // 按鈕點擊處理函數
  const handleButtonClick = (number) => {
    // 建立 WebSocket 連接
    const ws = new WebSocket('ws://49.213.238.75:8003/ws/chat/mouse/');

    ws.onopen = () => {
      console.log('WebSocket 連接成功！');
      // 將點擊的數字發送給 WebSocket 伺服器
      const message = {
        type: 'button_click',
        number: number.toString()
      };

      ws.send(JSON.stringify(message));
    };

    ws.onerror = (error) => {
      console.error('WebSocket 錯誤發生：', error);
    };

    // ws.onclose = () => {
    //   console.log('WebSocket 連接關閉！');
    // };
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center">
      <header className="App-header w-full max-w-md">
        <div className="button-container flex flex-col items-center space-y-16 w-full px-[10px]">
          <button className="number-button bg-gray-700 text-gray-200 text-2xl py-16 w-full rounded-lg" onClick={() => handleButtonClick(1)}>Next</button>
          <button className="number-button bg-gray-700 text-gray-200 text-2xl py-16 w-full rounded-lg" onClick={() => handleButtonClick(2)}>Prev</button>
          <button className="number-button bg-gray-700 text-gray-200 text-2xl py-16 w-full rounded-lg" onClick={() => handleButtonClick(3)}>Video</button>
        </div>
      </header>
    </div>
  );
}

export default App;
