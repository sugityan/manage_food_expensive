import { Button, Card, Input, Typography } from "@material-tailwind/react";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const UserRegister = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [age, setAge] = useState(0);
  const [household, setHousehold] = useState(0);
  const navigate = useNavigate();

  //   ログイン処理
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("https://example.com/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, age, household }),
      });

      //   response.okはレスポンスが200番台かどうかを判定する
      //   エラーの内容はとりあえず指定しない
      //   ユーザーIDはどうやって引き継ぐ？
      if (response.ok) {
        // ログイン成功
        console.log("ログイン成功");
        navigate("/home"); // /homeにリダイレクト
      } else {
        // ログイン失敗
        console.log("ログイン失敗");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <Card color="transparent" shadow={false}>
        <Typography variant="h4" color="blue-gray">
          Register
        </Typography>
        <form
          className="mt-8 mb-2 w-80 max-w-screen-lg sm:w-96"
          onSubmit={handleSubmit}
        >
          <div className="mb-4 flex flex-col gap-6">
            <Input
              size="lg"
              label="Email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
            <Input
              type="password"
              size="lg"
              label="Password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
            <Input
              type="number"
              size="lg"
              label="Age"
              value={age}
              onChange={(event) => setAge(parseInt(event.target.value))}
            />
            <Input
              type="number"
              size="lg"
              label="Household"
              value={household}
              onChange={(event) => setHousehold(parseInt(event.target.value))}
            />
          </div>
          <Button
            type="submit"
            className="mt-6"
            fullWidth
            onClick={handleSubmit}
          >
            Register
          </Button>
          <Typography color="gray" className="mt-4 text-center font-normal">
            Already have an account?{" "}
            <a
              href="/login"
              className="font-medium text-gray-900 border-b border-gray-600"
            >
              Login
            </a>
          </Typography>
        </form>
      </Card>
    </div>
  );
};

export default UserRegister;
