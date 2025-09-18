import axios from 'axios';

const realBaseURL = 'http://127.0.0.1:5000/api'; 

const request = axios.create({
    baseURL: realBaseURL,
    timeout: 10000
});

request.interceptors.request.use(config => {
  if (config.url && config.params) {
    const encodedParams = Object.entries(config.params).reduce((acc, [key, value]) => {
      acc[key] = typeof value === 'string' ? encodeURIComponent(value) : value;
      return acc;
    }, {} as Record<string, any>);
    config.params = encodedParams;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

request.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    if (error.response) {
      console.error('API Error:', {
        status: error.response.status,
        data: error.response.data,
        url: error.config.url
      });
      return Promise.reject(`服务器错误: ${error.response.status}`);
    } else if (error.request) {
      console.error('Network Error:', error.message);
      return Promise.reject('网络错误，请检查连接');
    } else {
      console.error('Request Error:', error.message);
      return Promise.reject('请求配置错误');
    }
  }
);

// 接口1: 获取所有省份的统计数据
export const getAllProvinceStats = () => {
    const url = '/data';
    return request.get(url);
}

// 接口2: 获取全国产量预测数据
export const getNationalPrediction = () => {
    const url = '/prediction/national';
    return request.get(url);
}

// 接口3: 获取特定省份和年份的城市y产量数据
export const getCityStats = (province: string, year: number) => {
    const url =  `/city/${year}/${province}`; 
    console.log(url);
    
    return request.get(url);
}

// 定义原始数据行的类型
export interface RawData {
  year: number;
  province: string;
  city?: string;
  county?: string;
  yield: number; 
}

// 接口4: 根据条件查询原始数据
export const getRawData = (params: { year?: number; province?: string }) => {
    return request.get('/raw_data', { params }); 
}

// 接口5: 更新或插入
export const upsertData = (data: RawData) => {
    return request.put('/raw_data', data); 
}

// 接口6: 删除 
export const deleteData = (data: { year: number; province: string; city?: string; county?: string }) => {
    return request.delete('/raw_data', { data });
}